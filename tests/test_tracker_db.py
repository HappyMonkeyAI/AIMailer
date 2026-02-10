import os
import sys
import pytest
from datetime import datetime, timedelta

# Setup paths
sys.path.append(os.path.join(os.getcwd(), 'src'))
sys.path.append(os.path.join(os.getcwd(), 'web'))

# Configure Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
import django
django.setup()

from newsletters.models import SentArticle
from aimailer import tracker
import importlib
importlib.reload(tracker)

@pytest.mark.django_db
def test_tracker_db_integration():
    # Clear DB
    SentArticle.objects.all().delete()

    # 1. Test save_sent_articles
    urls = {'http://example.com/1', 'http://example.com/2'}
    tracker.save_sent_articles(urls)

    assert SentArticle.objects.count() == 2
    assert SentArticle.objects.filter(url='http://example.com/1').exists()

    # 2. Test load_sent_articles
    loaded_urls = tracker.load_sent_articles()
    assert loaded_urls == urls

    # 3. Test filter_new_articles
    articles = [
        {'url': 'http://example.com/1'}, # Existing
        {'url': 'http://example.com/3'}, # New
        {'url': 'http://example.com/2'}, # Existing
    ]

    new_articles = tracker.filter_new_articles(articles)
    assert len(new_articles) == 1
    assert new_articles[0]['url'] == 'http://example.com/3'

    # 4. Test cleanup
    # Manually create an old article
    old_url = 'http://example.com/old'
    old_date = datetime.now() - timedelta(days=40)
    SentArticle.objects.create(url=old_url)
    SentArticle.objects.filter(url=old_url).update(sent_at=old_date)

    assert SentArticle.objects.filter(url=old_url).exists()

    # Trigger cleanup via save (tracker.py calls _clean_old_entries inside save_sent_articles,
    # but wait, my implementation calls _clean_old_entries() which uses SentArticle.objects.filter(...).delete())
    # Note: save_sent_articles only calls cleanup if HAS_DJANGO is True.

    tracker.save_sent_articles({'http://example.com/new'})

    # Verify old article is gone
    assert not SentArticle.objects.filter(url=old_url).exists()
    # Verify new article is there
    assert SentArticle.objects.filter(url='http://example.com/new').exists()

if __name__ == "__main__":
    # Manually run test if executed as script
    try:
        test_tracker_db_integration()
        print("Test passed!")
    except Exception as e:
        print(f"Test failed: {e}")
        import traceback
        traceback.print_exc()
