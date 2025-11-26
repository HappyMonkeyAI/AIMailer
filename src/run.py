import argparse
import importlib
import os
from typing import List


def fetch_sources(fetchers, config):
    items = []
    # Fetch configured DEFAULT_SOURCES (simple HTTP fetch + title heuristic)
    for url in getattr(config, 'DEFAULT_SOURCES', []):
        html = fetchers.fetch_http(url)
        title = url
        if html:
            # crude title extraction
            import re
            m = re.search(r'<title>(.*?)</title>', html, flags=re.IGNORECASE|re.DOTALL)
            if m:
                title = m.group(1).strip()
        items.append({'title': title, 'url': url, 'source': url, 'date': None, 'summary': ''})
    # Query local search endpoints if configured
    perplexica = os.environ.get('PERPLEXICA_URL', 'http://10.0.10.46:3030/discover')
    searx = os.environ.get('SEARXNG_URL', 'http://10.0.10.46:4040')
    keywords = getattr(config, 'KEYWORDS', [])
    q = ' '.join(keywords[:5]) if keywords else 'ai'
    # Perplexica (best-effort)
    try:
        r = fetchers.fetch_http(perplexica + '?q=' + q)
        if r:
            # If it returns HTML, skip parsing; if JSON, try loads
            import json
            try:
                data = json.loads(r)
                # expect list of results
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


def main(dry_run=True, max_items=12):
    fetchers = importlib.import_module('aimailer.fetchers')
    extractor = importlib.import_module('aimailer.extractor')
    summarizer = importlib.import_module('aimailer.summarizer')
    composer = importlib.import_module('aimailer.composer')
    sender = importlib.import_module('aimailer.sender')
    selector = importlib.import_module('aimailer.selector')
    config = importlib.import_module('aimailer.config')

    print('Running AIMailer pipeline (dry_run=%s)' % dry_run)
    raw_items = fetch_sources(fetchers, config)
    print('Fetched', len(raw_items), 'seed items')
    enriched = []
    for it in raw_items:
        url = it.get('url')
        html = fetchers.fetch_http(url) if url else None
        text = extractor.extract_text(html) if html else (it.get('summary') or '')
        summary_obj = summarizer.summarize_text(text)
        it['summary'] = summary_obj.get('summary','')
        it['why'] = summary_obj.get('why_dev_care','')
        it['tags'] = summary_obj.get('tags',[])
        it['confidence'] = summary_obj.get('confidence', 0.0)
        enriched.append(it)
    print('Enriched', len(enriched), 'items with summaries')
    source_weight_map = {'openai.com': 2.0, 'google': 1.5, 'anthropic': 1.5}
    top = selector.select_top(enriched, getattr(config, 'KEYWORDS', []), source_weight_map, n=max_items)
    print('Selected', len(top), 'top items')
    html_email = composer.compose_html('Weekly AI Tooling Roundup', top)
    sender.send_email('Weekly AI Tooling Roundup', html_email, getattr(config, 'RECIPIENT', 'stephen.z.phillips@sparktsl.com'), dry_run=dry_run)
    # Save sample output for inspection
    out_path = os.environ.get('AIMAILER_DRYOUT', 'aimailer_last_dryrun.html')
    with open(out_path, 'w') as f:
        f.write(html_email)
    print('Wrote dry-run HTML to', out_path)


if __name__ == '__main__':
    p = argparse.ArgumentParser()
    p.add_argument('--dry-run', action='store_true', dest='dry_run', default=True, help='Do not actually send email')
    p.add_argument('--max-items', type=int, default=12)
    args = p.parse_args()
    main(dry_run=args.dry_run, max_items=args.max_items)
