#!/usr/bin/env python3
"""Utility to manage the sent articles cache."""

import sys
import os
sys.path.insert(0, 'src')

from aimailer.tracker import load_sent_articles, CACHE_FILE
import json
from datetime import datetime

def show_cache():
    """Show current cache contents."""
    if not os.path.exists(CACHE_FILE):
        print("No cache file found.")
        return
    
    try:
        with open(CACHE_FILE, 'r') as f:
            data = json.load(f)
        
        print(f"Cache file: {CACHE_FILE}")
        print(f"Total articles: {len(data)}")
        print("\nRecent articles:")
        
        # Sort by date (newest first)
        sorted_items = sorted(data.items(), key=lambda x: x[1], reverse=True)
        
        for i, (url, date_str) in enumerate(sorted_items[:10]):
            try:
                date_obj = datetime.fromisoformat(date_str)
                print(f"{i+1:2d}. {date_obj.strftime('%Y-%m-%d %H:%M')} - {url}")
            except:
                print(f"{i+1:2d}. {date_str} - {url}")
        
        if len(data) > 10:
            print(f"... and {len(data) - 10} more")
            
    except Exception as e:
        print(f"Error reading cache: {e}")

def clear_cache():
    """Clear the article cache."""
    if os.path.exists(CACHE_FILE):
        os.remove(CACHE_FILE)
        print("Cache cleared.")
    else:
        print("No cache file to clear.")

def main():
    if len(sys.argv) < 2:
        print("Usage: python manage_cache.py [show|clear]")
        return
    
    command = sys.argv[1].lower()
    
    if command == 'show':
        show_cache()
    elif command == 'clear':
        clear_cache()
    else:
        print("Unknown command. Use 'show' or 'clear'.")

if __name__ == '__main__':
    main()
