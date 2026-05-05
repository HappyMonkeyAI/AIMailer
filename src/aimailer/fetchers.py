import requests
import feedparser
import socket
from urllib.parse import urlparse
from typing import List, Dict, Optional
from .feed_cache import FeedCache


def is_safe_url(url: str) -> bool:
    """Check if a URL is safe to fetch (prevents SSRF)."""
    try:
        parsed = urlparse(url)
        if parsed.scheme not in ('http', 'https'):
            return False
        
        hostname = parsed.hostname
        if not hostname:
            return False

        # Basic block for localhost and obvious private IPs
        if hostname in ('localhost', '127.0.0.1', '::1', '0.0.0.0'):
            return False

        # Resolve IP to check for private ranges
        ip = socket.gethostbyname(hostname)
        ip_parts = [int(x) for x in ip.split('.')]
        
        # Check for private IP ranges
        # 10.0.0.0/8
        if ip_parts[0] == 10:
            return False
        # 172.16.0.0/12
        if ip_parts[0] == 172 and 16 <= ip_parts[1] <= 31:
            return False
        # 192.168.0.0/16
        if ip_parts[0] == 192 and ip_parts[1] == 168:
            return False
        # 169.254.0.0/16 (Link-local)
        if ip_parts[0] == 169 and ip_parts[1] == 254:
            return False
            
        return True
    except Exception:
        return False


def fetch_http(url: str, timeout: int = 10) -> Optional[str]:
    """Return text content for a GET request or None on failure."""
    if not is_safe_url(url):
        print(f"Blocked unsafe URL: {url}")
        return None

    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36'
    }
    try:
        r = requests.get(url, timeout=timeout, headers=headers)
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
    if not is_safe_url(url):
        print(f"Blocked unsafe RSS URL: {url}")
        return []

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
