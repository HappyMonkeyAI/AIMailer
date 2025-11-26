import requests
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
    """Placeholder: fetch an RSS feed and return list of items with title/url/summary/date."""
    # Implement RSS parsing (feedparser) in later iteration.
    return []
