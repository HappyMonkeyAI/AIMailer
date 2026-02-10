import os
import sys
import json
import pytest
from datetime import datetime, timedelta
import importlib

# Setup paths
sys.path.append(os.path.join(os.getcwd(), 'src'))
sys.path.append(os.path.join(os.getcwd(), 'web'))

# Configure Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
import django
django.setup()

from newsletters.models import SentArticle
from aimailer import tracker

@pytest.mark.django_db
def test_migration_from_file_to_db():
    # 1. Setup: Create JSON file and clear DB
    test_cache = 'test_migration_sent_articles.json'

    # Reload tracker to reset _MIGRATION_DONE flag
    importlib.reload(tracker)

    SentArticle.objects.all().delete()

    data = {}
    now = datetime.now()
    url1 = 'http://example.com/migrated1'
    url2 = 'http://example.com/migrated2'
    url_old = 'http://example.com/old'

    data[url1] = now.isoformat()
    data[url2] = (now - timedelta(days=1)).isoformat()
    data[url_old] = (now - timedelta(days=60)).isoformat() # Should be cleaned up

    with open(test_cache, 'w') as f:
        json.dump(data, f)

    try:
        # 2. Trigger migration via load_sent_articles
        # Verify DB is empty before
        assert SentArticle.objects.count() == 0

        # Pass cache_file explicitly
        tracker.load_sent_articles(test_cache)

        # 3. Verify DB populated
        assert SentArticle.objects.count() == 2 # url_old should be skipped
        assert SentArticle.objects.filter(url=url1).exists()
        assert SentArticle.objects.filter(url=url2).exists()
        assert not SentArticle.objects.filter(url=url_old).exists()

        # 4. Verify repeated call doesn't migrate again (or handles duplicates via ignore_conflicts)
        tracker._MIGRATION_DONE = False # Force check again
        tracker.load_sent_articles(test_cache)
        assert SentArticle.objects.count() == 2

    finally:
        if os.path.exists(test_cache):
            os.remove(test_cache)

if __name__ == "__main__":
    try:
        test_migration_from_file_to_db()
        print("Migration test passed!")
    except Exception as e:
        print(f"Migration test failed: {e}")
        import traceback
        traceback.print_exc()
