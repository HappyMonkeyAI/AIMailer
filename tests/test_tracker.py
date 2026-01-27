import unittest
import os
import json
import shutil
from aimailer import tracker

class TestTracker(unittest.TestCase):

    def setUp(self):
        self.test_cache = 'test_sent_articles.json'
        # Ensure clean state
        if os.path.exists(self.test_cache):
            os.remove(self.test_cache)

    def tearDown(self):
        if os.path.exists(self.test_cache):
            os.remove(self.test_cache)

    def test_save_and_load(self):
        urls = {'http://example.com/1', 'http://example.com/2'}
        tracker.save_sent_articles(urls, self.test_cache)

        loaded = tracker.load_sent_articles(self.test_cache)
        self.assertEqual(urls, loaded)

    def test_filter_new_articles(self):
        tracker.save_sent_articles({'http://old.com'}, self.test_cache)

        articles = [
            {'url': 'http://old.com', 'title': 'Old'},
            {'url': 'http://new.com', 'title': 'New'}
        ]

        filtered = tracker.filter_new_articles(articles, self.test_cache)
        self.assertEqual(len(filtered), 1)
        self.assertEqual(filtered[0]['url'], 'http://new.com')

    def test_mark_articles_sent(self):
        articles = [{'url': 'http://a.com'}, {'url': 'http://b.com'}]
        tracker.mark_articles_sent(articles, self.test_cache)

        loaded = tracker.load_sent_articles(self.test_cache)
        self.assertEqual(len(loaded), 2)
        self.assertIn('http://a.com', loaded)

if __name__ == '__main__':
    unittest.main()
