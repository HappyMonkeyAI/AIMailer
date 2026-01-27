import unittest
from aimailer import extractor
import bleach

class TestExtractor(unittest.TestCase):

    def test_extract_text_sanitization(self):
        # Must be > 20 chars
        html = "<script>alert('xss')</script><p>Hello this is a very long sentence that should pass the filter.</p>"
        text = extractor.extract_text(html)
        self.assertNotIn('script', text)
        self.assertNotIn('alert', text)
        self.assertIn('Hello this is a very long sentence', text)

    def test_extract_text_noise_removal(self):
        html = "<p>Some content that is definitely long enough to be kept by the extractor logic. Skip to main content. More content that is also long enough to be kept.</p>"
        text = extractor.extract_text(html)
        self.assertNotIn('Skip to main content', text)
        self.assertIn('Some content that is definitely long enough', text)

    def test_extract_text_empty(self):
        self.assertEqual(extractor.extract_text(None), '')
        self.assertEqual(extractor.extract_text(''), '')

    def test_extract_text_links(self):
        html = '<a href="http://example.com">Link to a website that has a long description text inside it</a>'
        text = extractor.extract_text(html)
        self.assertIn('Link to a website', text)
        self.assertNotIn('href', text)

if __name__ == '__main__':
    unittest.main()
