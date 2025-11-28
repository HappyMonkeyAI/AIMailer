import os
import json
from datetime import datetime, timedelta
from typing import List, Dict, Set

DEFAULT_CACHE_FILE = '/var/www/html/happymonkey.ai/AIMailer/sent_articles.json'
CACHE_DAYS = 30  # Keep track for 30 days


def load_sent_articles(cache_file: str = None) -> Set[str]:
    """Load previously sent article URLs from cache."""
    cache_file = cache_file or DEFAULT_CACHE_FILE
    if not os.path.exists(cache_file):
        return set()
    
    try:
        with open(cache_file, 'r') as f:
            data = json.load(f)
        
        # Clean old entries (older than CACHE_DAYS)
        cutoff = datetime.now() - timedelta(days=CACHE_DAYS)
        current_urls = set()
        
        for url, date_str in data.items():
            try:
                sent_date = datetime.fromisoformat(date_str)
                if sent_date > cutoff:
                    current_urls.add(url)
            except:
                continue
        
        return current_urls
    except:
        return set()


def save_sent_articles(sent_urls: Set[str], cache_file: str = None) -> None:
    """Save sent article URLs to cache with current timestamp."""
    cache_file = cache_file or DEFAULT_CACHE_FILE
    try:
        # Load existing data
        existing_data = {}
        if os.path.exists(cache_file):
            try:
                with open(cache_file, 'r') as f:
                    existing_data = json.load(f)
            except:
                pass
        
        # Add new URLs with current timestamp
        current_time = datetime.now().isoformat()
        for url in sent_urls:
            existing_data[url] = current_time
        
        # Clean old entries
        cutoff = datetime.now() - timedelta(days=CACHE_DAYS)
        cleaned_data = {}
        for url, date_str in existing_data.items():
            try:
                sent_date = datetime.fromisoformat(date_str)
                if sent_date > cutoff:
                    cleaned_data[url] = date_str
            except:
                continue
        
        # Save to file
        with open(cache_file, 'w') as f:
            json.dump(cleaned_data, f, indent=2)
    except Exception as e:
        print(f'Warning: Could not save article cache: {e}')


def filter_new_articles(articles: List[Dict], cache_file: str = None) -> List[Dict]:
    """Filter out articles that have been sent before."""
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
