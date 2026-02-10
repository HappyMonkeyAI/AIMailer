import os
import json
import logging
from datetime import datetime, timedelta
from typing import List, Dict, Set

# Try to import Django models
try:
    from newsletters.models import SentArticle
    HAS_DJANGO = True
except ImportError:
    HAS_DJANGO = False

DEFAULT_CACHE_FILE = '/var/www/html/happymonkey.ai/AIMailer/sent_articles.json'
CACHE_DAYS = 30  # Keep track for 30 days
logger = logging.getLogger(__name__)

_MIGRATION_DONE = False

def migrate_from_file_to_db(cache_file: str = None) -> None:
    """Populate DB from file if DB is empty."""
    global _MIGRATION_DONE
    if _MIGRATION_DONE:
        return

    if not HAS_DJANGO:
        return

    try:
        # Check if DB is empty (efficient check)
        if SentArticle.objects.exists():
            _MIGRATION_DONE = True
            return

        logger.info("Database sent_articles empty, checking for file cache to migrate...")
        cache_file = cache_file or DEFAULT_CACHE_FILE
        if not os.path.exists(cache_file):
            _MIGRATION_DONE = True
            return

        try:
            with open(cache_file, 'r') as f:
                data = json.load(f)
        except Exception:
            _MIGRATION_DONE = True
            return

        # Clean old entries
        cleaned_data = _clean_old_entries_file(data)

        # Insert into DB
        count = 0
        batch_size = 1000
        urls = list(cleaned_data.keys())
        for i in range(0, len(urls), batch_size):
            batch = urls[i:i+batch_size]
            objs = []
            for url in batch:
                try:
                    dt = datetime.fromisoformat(cleaned_data[url])
                    # Make naive datetime aware if needed, but Django handles naive usually as local time
                    # or fails if timezone support is on.
                    # Best to assume naive is okay or use timezone.make_aware if settings.USE_TZ
                    objs.append(SentArticle(url=url, sent_at=dt))
                except Exception:
                    continue

            SentArticle.objects.bulk_create(objs, ignore_conflicts=True)
            count += len(objs)

        logger.info(f"Migrated {count} entries from file cache to database.")
        _MIGRATION_DONE = True
    except Exception as e:
        logger.error(f"Migration failed: {e}")


def _clean_old_entries_file(data: Dict[str, str], days: int = CACHE_DAYS) -> Dict[str, str]:
    """Remove entries older than the specified number of days (File version)."""
    cutoff = datetime.now() - timedelta(days=days)
    cleaned_data = {}
    for url, date_str in data.items():
        try:
            sent_date = datetime.fromisoformat(date_str)
            if sent_date > cutoff:
                cleaned_data[url] = date_str
        except Exception:
            continue
    return cleaned_data


def load_sent_articles(cache_file: str = None) -> Set[str]:
    """Load previously sent article URLs from cache."""
    if HAS_DJANGO:
        try:
            migrate_from_file_to_db(cache_file)
            cutoff = datetime.now() - timedelta(days=CACHE_DAYS)
            return set(SentArticle.objects.filter(sent_at__gt=cutoff).values_list('url', flat=True))
        except Exception as e:
            logger.error(f"Error loading sent articles from DB: {e}")
            # Fallback to file if DB fails?
            pass

    cache_file = cache_file or DEFAULT_CACHE_FILE
    if not os.path.exists(cache_file):
        return set()
    
    try:
        with open(cache_file, 'r') as f:
            data = json.load(f)
        
        cleaned_data = _clean_old_entries_file(data)
        return set(cleaned_data.keys())
    except Exception:
        return set()


def save_sent_articles(sent_urls: Set[str], cache_file: str = None) -> None:
    """Save sent article URLs to cache with current timestamp."""
    if HAS_DJANGO:
        try:
            migrate_from_file_to_db(cache_file)
            # Create new entries
            for url in sent_urls:
                # Use get_or_create to avoid duplicates
                SentArticle.objects.get_or_create(url=url)

            # Clean old entries
            cutoff = datetime.now() - timedelta(days=CACHE_DAYS)
            SentArticle.objects.filter(sent_at__lt=cutoff).delete()
            return
        except Exception as e:
            logger.error(f"Error saving sent articles to DB: {e}")
            print(f'Warning: Could not save article cache to DB: {e}')
            # Fallback to file

    cache_file = cache_file or DEFAULT_CACHE_FILE
    try:
        # Load existing data
        existing_data = {}
        if os.path.exists(cache_file):
            try:
                with open(cache_file, 'r') as f:
                    existing_data = json.load(f)
            except Exception:
                pass
        
        # Add new URLs with current timestamp
        current_time = datetime.now().isoformat()
        for url in sent_urls:
            existing_data[url] = current_time
        
        # Clean old entries
        cleaned_data = _clean_old_entries_file(existing_data)
        
        # Save to file
        with open(cache_file, 'w') as f:
            json.dump(cleaned_data, f, indent=2)
    except Exception as e:
        print(f'Warning: Could not save article cache to file: {e}')


def filter_new_articles(articles: List[Dict], cache_file: str = None) -> List[Dict]:
    """Filter out articles that have been sent before."""
    if HAS_DJANGO:
        try:
            migrate_from_file_to_db(cache_file)
            urls_to_check = [a.get('url') for a in articles if a.get('url')]
            if not urls_to_check:
                return articles

            # Efficient query: only get URLs that exist in DB
            # We fetch all matching URLs in one query
            existing_urls = set(SentArticle.objects.filter(url__in=urls_to_check).values_list('url', flat=True))

            new_articles = []
            for article in articles:
                url = article.get('url', '')
                if url and url not in existing_urls:
                    new_articles.append(article)
            return new_articles
        except Exception as e:
            logger.error(f"Error filtering articles with DB: {e}")
            # Fallback to load_sent_articles (which might fallback to file)

    sent_urls = load_sent_articles(cache_file)
    new_articles = []
    
    for article in articles:
        url = article.get('url', '')
        if url and url not in sent_urls:
            new_articles.append(article)
    
    return new_articles


def mark_articles_sent(articles: List[Dict], cache_file: str = None) -> None:
    """Mark articles as sent to prevent future duplicates."""
    urls = {article.get('url') for article in articles if article.get('url')}
    urls.discard(None)  # Remove None values
    save_sent_articles(urls, cache_file)
