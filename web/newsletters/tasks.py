import sys
import os
import json
import logging
from pathlib import Path
from celery import shared_task
from django.utils import timezone
from django.conf import settings

# Add src to sys.path to import aimailer modules
BASE_DIR = Path(__file__).resolve().parent.parent.parent
SRC_DIR = BASE_DIR / 'src'
if str(SRC_DIR) not in sys.path:
    sys.path.append(str(SRC_DIR))

try:
    from aimailer import fetchers, extractor, summarizer, composer, sender, selector, tracker
    HAS_AIMAILER = True
except ImportError as e:
    HAS_AIMAILER = False
    print(f"Warning: Could not import aimailer modules: {e}")

from .models import Newsletter, SendHistory, Subscriber

logger = logging.getLogger(__name__)

class NewsletterConfigAdapter:
    """Adapter to make Newsletter/Config models look like the config module expected by aimailer."""
    def __init__(self, newsletter):
        self.newsletter = newsletter
        self.config = newsletter.config

        # Extract settings
        self.DEFAULT_SOURCES = [s.url for s in newsletter.rss_sources.filter(is_active=True)]
        self.KEYWORDS = newsletter.keywords

        # Email settings
        self.EMAIL_TITLE = newsletter.title
        self.EMAIL_SUBJECT = self.config.config_json.get('email_subject', f"{newsletter.title} - {timezone.now().strftime('%Y-%m-%d')}")

        # Recipients (active subscribers)
        self.RECIPIENTS = [s.email for s in newsletter.subscribers.filter(status='active')]

        # Other settings
        self.CACHE_FILE = None # Use DB tracking

        # Extra config from JSON
        for k, v in self.config.config_json.items():
            if k not in ['email_subject', 'dry_run', 'source_weights']:
                setattr(self, k.upper(), v)


@shared_task(bind=True)
def process_newsletter(self, newsletter_id):
    """
    Celery task to process and send a newsletter.
    """
    if not HAS_AIMAILER:
        logger.error("AIMailer modules not found. Cannot process newsletter.")
        return

    # Implementation of a distributed lock using Redis to prevent concurrent executions
    from django.core.cache import cache
    lock_id = f"newsletter_lock_{newsletter_id}"
    # acquire_lock = cache.add(lock_id, "true", 3600*4) # Lock for 4 hours
    # if not acquire_lock:
    #     logger.warning(f"Newsletter {newsletter_id} is already being processed by another worker. Skipping.")
    #     return

    # Use a context manager for more robust locking if available, 
    # but cache.add is the standard way to implement a simple lock in Django.
    if not cache.add(lock_id, self.request.id, 3600*4):
        logger.warning(f"Newsletter {newsletter_id} is already being processed. Skipping task {self.request.id}")
        return

    try:
        newsletter = Newsletter.objects.get(id=newsletter_id)
        config = newsletter.config
    except Newsletter.DoesNotExist:
        logger.error(f"Newsletter {newsletter_id} not found.")
        return
    except Exception as e:
        logger.error(f"Error loading newsletter {newsletter_id}: {e}")
        return

    logger.info(f"Starting processing for newsletter: {newsletter.title}")

    # Create config adapter
    conf = NewsletterConfigAdapter(newsletter)

    # Check if there are recipients
    if not conf.RECIPIENTS:
        logger.info(f"No active subscribers for {newsletter.title}. Skipping.")
        return

    # Check for dry run override in config_json
    dry_run = config.config_json.get('dry_run', False)

    try:
        # 1. Fetch Sources
        items = []
        for url in conf.DEFAULT_SOURCES:
            try:
                # We can use a shared feed cache file or None
                rss_items = fetchers.fetch_rss(url, cache_file=None)
                items.extend(rss_items)
            except Exception as e:
                logger.warning(f"Error fetching {url}: {e}")

        # Query local search endpoints if configured
        perplexica = os.environ.get('PERPLEXICA_URL', 'http://localhost:3030/discover')
        searx = os.environ.get('SEARXNG_URL', 'http://localhost:4040')
        keywords = conf.KEYWORDS
        q = ' '.join(keywords[:5]) if keywords else 'ai'

        # Perplexica (best-effort)
        try:
            r = fetchers.fetch_http(perplexica + '?q=' + q)
            if r:
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
                try:
                    data = json.loads(r)
                    for it in data.get('results', [])[:8]:
                        items.append({'title': it.get('title') or '', 'url': it.get('url') or it.get('link'), 'source': 'searxng', 'date': it.get('published'), 'summary': it.get('content') or ''})
                except Exception:
                    pass
        except Exception:
            pass

        logger.info(f"Fetched {len(items)} items.")

        # 2. Filter New Articles
        # tracker.filter_new_articles uses DB if imported correctly (which it is)
        new_items = tracker.filter_new_articles(items, cache_file=None)
        logger.info(f"Filtered to {len(new_items)} new articles.")

        if not new_items:
            logger.info("No new articles found.")
            return

        # 3. Process Items (Summarize)
        enriched = []
        # Sequential processing for simplicity in Celery (or use sub-tasks?)
        # src/run.py uses ThreadPoolExecutor. We can do that too.
        import concurrent.futures

        def _process(item):
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
                logger.error(f"Error processing item {item.get('url')}: {e}")
                return item

        # Limit workers
        max_workers = min(10, len(new_items))
        with concurrent.futures.ThreadPoolExecutor(max_workers=max_workers) as executor:
            future_to_item = {executor.submit(_process, item): item for item in new_items}
            for future in concurrent.futures.as_completed(future_to_item):
                try:
                    res = future.result()
                    enriched.append(res)
                except Exception:
                    pass

        logger.info(f"Enriched {len(enriched)} items.")

        # 4. Select Top Items
        source_weights = config.config_json.get('source_weights', {'openai.com': 2.0, 'google': 1.5})
        top_items = selector.select_top(enriched, conf.KEYWORDS, source_weights, n=config.article_count)

        if not top_items:
            logger.info("No suitable articles selected.")
            return

        # 5. Compose Email
        html_email = composer.compose_html(conf.EMAIL_TITLE, top_items)

        # Build recipient list with unsubscribe URLs
        site_url = getattr(settings, 'SITE_URL', 'http://localhost:8000').rstrip('/')
        recipients_list = []
        for sub in newsletter.subscribers.filter(status='active'):
            unsub_url = f"{site_url}/newsletter/unsubscribe/{sub.unsubscribe_token}/"
            recipients_list.append({
                'email': sub.email,
                'unsubscribe_url': unsub_url
            })

        # 6. Send Email
        sent_count = sender.send_email(
            conf.EMAIL_SUBJECT,
            html_email,
            recipients_list,
            dry_run=dry_run,
            sender_email=config.sender_email,
            sender_name=config.sender_name
        )

        # 7. Mark as Sent
        if (sent_count > 0 or dry_run):
            tracker.mark_articles_sent(top_items, cache_file=None)

        # 8. Record History
        success_count = sent_count if not dry_run else len(recipients_list)
        failure_count = len(recipients_list) - success_count

        SendHistory.objects.create(
            newsletter=newsletter,
            recipient_count=len(recipients_list),
            success_count=success_count,
            failure_count=failure_count,
            articles_sent=[item.get('url') for item in top_items],
            celery_task_id=self.request.id or ''
        )

        logger.info(f"Newsletter {newsletter.title} processed. Sent: {success_count}/{len(recipients_list)}")

    except Exception as e:
        logger.error(f"Error in process_newsletter: {e}", exc_info=True)
        # Create failure history
        count = len(recipients_list) if 'recipients_list' in locals() else (len(conf.RECIPIENTS) if 'conf' in locals() else 0)
        SendHistory.objects.create(
            newsletter=newsletter,
            recipient_count=count,
            success_count=0,
            failure_count=count,
            celery_task_id=self.request.id or '',
            articles_sent=[]
        )
    finally:
        # Always release the lock
        cache.delete(lock_id)
        logger.info(f"Released lock for newsletter {newsletter_id}")
