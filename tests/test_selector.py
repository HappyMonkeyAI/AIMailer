import unittest
from aimailer import selector

class TestSelector(unittest.TestCase):

    def test_dedupe(self):
        items = [
            {'url': 'http://a.com', 'title': 'A'},
            {'url': 'http://a.com', 'title': 'A duplicate'},
            {'url': 'http://b.com', 'title': 'B'}
        ]
        deduped = selector.dedupe(items)
        self.assertEqual(len(deduped), 2)
        urls = [i['url'] for i in deduped]
        self.assertIn('http://a.com', urls)
        self.assertIn('http://b.com', urls)

    def test_score_item(self):
        item = {'title': 'Python AI', 'summary': 'Coding with AI', 'source': 'openai.com'}
        keywords = ['python', 'ai']
        source_weights = {'openai.com': 2.0}

        score = selector.score_item(item, keywords, source_weights)
        # title+summary has 'python' and 'ai' -> +2.0
        # source 'openai.com' -> +2.0
        # total should be around 4.0 (ignoring date/confidence logic for this simple test)
        self.assertGreater(score, 3.0)

    def test_select_top_diverse(self):
        items = [
            {'url': 'http://1.com', 'source': 'A', 'title': '1', 'summary': 'key'},
            {'url': 'http://2.com', 'source': 'A', 'title': '2', 'summary': 'key'},
            {'url': 'http://3.com', 'source': 'B', 'title': '3', 'summary': 'key'},
        ]
        # Should pick from A then B then A
        selected = selector.select_top_diverse(items, ['key'], n=3)
        self.assertEqual(len(selected), 3)
        self.assertEqual(selected[0]['source'], 'A')
        self.assertEqual(selected[1]['source'], 'B')
        self.assertEqual(selected[2]['source'], 'A')

if __name__ == '__main__':
    unittest.main()
