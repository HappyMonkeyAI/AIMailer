import requests
import feedparser
from typing import List, Dict, Optional


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


def fetch_rss(url: str) -> List[Dict]:
    """Fetch an RSS feed and return list of items with title/url/summary/date."""
    try:
        feed = feedparser.parse(url)
        if hasattr(feed, 'bozo_exception') and feed.bozo_exception:
            print(f"Feed error for {url}: {feed.bozo_exception}")
            # Continue if we got some entries despite the error

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
