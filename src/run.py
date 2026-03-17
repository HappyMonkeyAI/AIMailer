import argparse
import importlib
import os
import sys
import django
import concurrent.futures
from dotenv import load_dotenv
load_dotenv()
from typing import List, Dict

# Setup Django environment
sys.path.append(os.path.join(os.path.dirname(__file__), '../web'))
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
django.setup()


def fetch_sources(fetchers, config, feed_cache_file=None):
    items = []
    # Fetch RSS feeds from configured sources
    for url in getattr(config, 'DEFAULT_SOURCES', []):
        rss_items = fetchers.fetch_rss(url, cache_file=feed_cache_file)
        print(f'Fetched {len(rss_items)} items from {url}')
        items.extend(rss_items)
    
    # Query local search endpoints if configured
    perplexica = os.environ.get('PERPLEXICA_URL', 'http://localhost:3030/discover')
    searx = os.environ.get('SEARXNG_URL', 'http://192.168.1.2:4040')
    keywords = getattr(config, 'KEYWORDS', [])
    q = ' '.join(keywords[:5]) if keywords else 'ai'
    
    # Perplexica (best-effort)
    try:
        r = fetchers.fetch_http(perplexica + '?q=' + q)
        if r:
            import json
            try:
                data = json.loads(r)
                for it in data.get('results', [])[:5]:
                    items.append({'title': it.get('title') or it.get('name') or '', 'url': it.get('url'), 'source': 'perplexica', 'date': it.get('date'), 'summary': it.get('snippet') or ''})
            except Exception:
                pass
    except Exception:
        pass
    
    # Searxng
    try:
        r = fetchers.fetch_http(searx.rstrip('/') + '/search?q=' + q + '&format=json')
        if r:
            import json
            try:
                data = json.loads(r)
                for it in data.get('results', [])[:8]:
                    items.append({'title': it.get('title') or '', 'url': it.get('url') or it.get('link'), 'source': 'searxng', 'date': it.get('published'), 'summary': it.get('content') or ''})
            except Exception:
                pass
    except Exception:
        pass
    return items


def process_item(item, fetchers, extractor, summarizer):
    """Fetch content, extract text, and summarize a single item."""
    try:
        url = item.get('url')
        html = fetchers.fetch_http(url) if url else None
        text = extractor.extract_text(html) if html else (item.get('summary') or '')
        summary_obj = summarizer.summarize_text(text)

        item['summary'] = summary_obj.get('summary', '')
        item['why'] = summary_obj.get('why_dev_care', '')
        item['tags'] = summary_obj.get('tags', [])
        item['confidence'] = summary_obj.get('confidence', 0.0)
        return item
    except Exception as e:
        print(f"Error processing item {item.get('url')}: {e}")
        return item


def main(dry_run=False, max_items=12, config_name='config'):
    fetchers = importlib.import_module('aimailer.fetchers')
    extractor = importlib.import_module('aimailer.extractor')
    summarizer = importlib.import_module('aimailer.summarizer')
    composer = importlib.import_module('aimailer.composer')
    sender = importlib.import_module('aimailer.sender')
    selector = importlib.import_module('aimailer.selector')
    tracker = importlib.import_module('aimailer.tracker')
    config = importlib.import_module(f'aimailer.{config_name}')

    print(f'Running AIMailer pipeline (config={config_name}, dry_run={dry_run})')

    # Filter out previously sent articles using config-specific cache
    cache_file = getattr(config, 'CACHE_FILE', None)

    # Derive feed cache path from sent articles cache path
    feed_cache_file = None
    if cache_file:
        try:
            from pathlib import Path
            feed_cache_file = str(Path(cache_file).parent / 'feed_metadata.json')
        except Exception:
            pass

    raw_items = fetch_sources(fetchers, config, feed_cache_file=feed_cache_file)
    print('Fetched', len(raw_items), 'seed items')

    new_items = tracker.filter_new_articles(raw_items, cache_file)
    print('Filtered to', len(new_items), 'new articles (removed', len(raw_items) - len(new_items), 'duplicates)')
    
    enriched = []
    # Use ThreadPoolExecutor to process items in parallel
    max_workers = min(10, len(new_items)) if len(new_items) > 0 else 1
    with concurrent.futures.ThreadPoolExecutor(max_workers=max_workers) as executor:
        future_to_item = {
            executor.submit(process_item, item, fetchers, extractor, summarizer): item
            for item in new_items
        }
        for future in concurrent.futures.as_completed(future_to_item):
            try:
                result = future.result()
                enriched.append(result)
            except Exception as e:
                print(f"Item processing generated an exception: {e}")

    print('Enriched', len(enriched), 'items with summaries')
    
    source_weight_map = {'openai.com': 2.0, 'google': 1.5, 'anthropic': 1.5, 'huggingface': 2.0, 'microsoft': 1.5}
    top = selector.select_top(enriched, getattr(config, 'KEYWORDS', []), source_weight_map, n=max_items)
    print('Selected', len(top), 'top items')
    
    if not top:
        print('No new articles to send today')
        return
    
    email_title = getattr(config, 'EMAIL_TITLE', 'AI Roundup')
    email_subject = getattr(config, 'EMAIL_SUBJECT', 'AI Roundup')
    recipients = getattr(config, 'RECIPIENTS', ['stephen.z.phillips@sparktsl.com'])
    
    html_email = composer.compose_html(email_title, top)
    sender.send_email(email_subject, html_email, recipients, dry_run=dry_run)
    
    # Mark articles as sent (only if not dry run)
    if not dry_run:
        tracker.mark_articles_sent(top, cache_file)
        print('Marked', len(top), 'articles as sent')
    
    # Save sample output for inspection
    out_path = os.environ.get('AIMAILER_DRYOUT', f'aimailer_last_dryrun_{config_name}.html')
    with open(out_path, 'w') as f:
        f.write(html_email)
    print('Wrote dry-run HTML to', out_path)


if __name__ == '__main__':
    p = argparse.ArgumentParser()
    p.add_argument('--dry-run', action='store_true', dest='dry_run', default=False, help='Do not actually send email')
    p.add_argument('--max-items', type=int, default=12)
    p.add_argument('--config', type=str, default='config', help='Config module name (config or config_models)')
    args = p.parse_args()
    main(dry_run=args.dry_run, max_items=args.max_items, config_name=args.config)
