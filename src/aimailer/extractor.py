import bleach
import re


def extract_text(html: str) -> str:
    """Extract clean article text from HTML using bleach for sanitization."""
    if not html:
        return ''
    
    # Pre-clean: Remove script and style tags AND their content completely.
    # Bleach with strip=True removes the tags but leaves the content (e.g. <script>foo</script> -> foo).
    html = re.sub(r'<script[^>]*>.*?</script>', '', html, flags=re.DOTALL | re.IGNORECASE)
    html = re.sub(r'<style[^>]*>.*?</style>', '', html, flags=re.DOTALL | re.IGNORECASE)
    
    # Allowed tags and attributes for initial cleaning
    allowed_tags = ['p', 'div', 'br', 'li', 'h1', 'h2', 'h3', 'h4', 'h5', 'h6', 'article', 'section', 'b', 'i', 'u', 'em', 'strong', 'a']
    allowed_attrs = {'a': ['href', 'title']}
    
    # Sanitize HTML
    clean_html = bleach.clean(html, tags=allowed_tags, attributes=allowed_attrs, strip=True)
    
    # Remove navigation and UI elements (still useful to remove noise text)
    noise_patterns = [
        r'Skip to main content',
        r'The Keyword',
        r'Share Twitter Facebook LinkedIn Mail Copy link',
        r'Home Product news',
        r'Product news',
        r'window\.[A-Z_]+',
        r'const \w+',
        r'document\.',
        r'"@context"',
        r'licenseKey:',
        r'applicationID:',
        r'browserID:'
    ]

    text = clean_html
    for pattern in noise_patterns:
        text = re.sub(pattern, '', text, flags=re.IGNORECASE)
    
    # Replace block tags with newlines for text extraction
    text = re.sub(r'</?(p|div|br|li|h[1-6]|article|section)[^>]*>', '\n', text, flags=re.IGNORECASE)

    # Remove remaining tags (strip=True removes tags, leaves content, but we are just removing allowed tags now)
    text = bleach.clean(text, tags=[], strip=True)

    # Clean up whitespace
    text = re.sub(r'\s+', ' ', text).strip()

    # Split into sentences and keep only meaningful ones
    sentences = re.split(r'[.!?]+', text)
    clean_sentences = []
    
    for sentence in sentences:
        sentence = sentence.strip()
        if (len(sentence) > 20 and  # Minimum length
            not sentence.startswith('{') and
            not sentence.startswith('window') and
            not sentence.startswith('const') and
            not sentence.startswith('document') and
            '"@' not in sentence and
            'licenseKey' not in sentence and
            len([c for c in sentence if c.isalpha()]) > len(sentence) * 0.7):  # Mostly letters
            clean_sentences.append(sentence)
    
    return '. '.join(clean_sentences[:10])  # Max 10 sentences
