import requests
import feedparser
from typing import List, Dict, Optional


def fetch_http(url: str, timeout: int = 10) -> Optional[str]:
    """Return text content for a GET request or None on failure."""
    try:
        r = requests.get(url, timeout=timeout)
        r.raise_for_status()
        return r.text
    except Exception:
        return None


def fetch_rss(url: str) -> List[Dict]:
    """Fetch an RSS feed and return list of items with title/url/summary/date."""
    try:
        feed = feedparser.parse(url)
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
    except Exception:
        return []
