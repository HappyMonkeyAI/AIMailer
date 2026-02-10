import requests
import feedparser
from typing import List, Dict, Optional
from .feed_cache import FeedCache


def fetch_http(url: str, timeout: int = 10) -> Optional[str]:
    """Return text content for a GET request or None on failure."""
    try:
        r = requests.get(url, timeout=timeout)
        r.raise_for_status()
        return r.text
    except requests.RequestException as e:
        print(f"Error fetching {url}: {e}")
        return None
    except Exception as e:
        print(f"Unexpected error fetching {url}: {e}")
        return None


def fetch_rss(url: str, cache_file: Optional[str] = None) -> List[Dict]:
    """Fetch an RSS feed and return list of items with title/url/summary/date."""
    try:
        etag = None
        modified = None
        cache = None

        if cache_file:
            try:
                cache = FeedCache(cache_file)
                etag, modified = cache.get(url)
            except Exception as e:
                # Cache failure should not stop fetching
                print(f"Cache load error for {url}: {e}")

        feed = feedparser.parse(url, etag=etag, modified=modified)

        # Handle 304 Not Modified
        if getattr(feed, 'status', 200) == 304:
            print(f"Feed {url} not modified (304).")
            return []

        if hasattr(feed, 'bozo_exception') and feed.bozo_exception:
            print(f"Feed error for {url}: {feed.bozo_exception}")
            # Continue if we got some entries despite the error

        # Update cache on success
        if cache and getattr(feed, 'status', 200) == 200:
            new_etag = getattr(feed, 'etag', None)
            new_modified = getattr(feed, 'modified', None)
             if new_etag or new_modified:
                 try:
                     cache.update(url, new_etag, new_modified)
                 except Exception as e:
                     print(f"Cache save error for {url}: {e}")

        items = []
        for entry in feed.entries[:50]:  # Limit to 50 most recent
            items.append({
                'title': getattr(entry, 'title', ''),
                'url': getattr(entry, 'link', ''),
                'summary': getattr(entry, 'summary', ''),
                'date': getattr(entry, 'published', None),
                'source': url
            })
        return items
    except Exception as e:
        print(f"Error parsing feed {url}: {e}")
        return []
