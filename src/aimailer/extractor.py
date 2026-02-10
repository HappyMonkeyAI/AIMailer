import bleach
import re

# Pre-compiled regexes for performance
SCRIPT_REGEX = re.compile(r'<script[^>]*>.*?</script>', flags=re.DOTALL | re.IGNORECASE)
STYLE_REGEX = re.compile(r'<style[^>]*>.*?</style>', flags=re.DOTALL | re.IGNORECASE)
BLOCK_TAGS_REGEX = re.compile(r'</?(p|div|br|li|h[1-6]|article|section)[^>]*>', flags=re.IGNORECASE)
WHITESPACE_REGEX = re.compile(r'\s+')
SENTENCE_SPLIT_REGEX = re.compile(r'[.!?]+')

NOISE_PATTERNS = [
    re.compile(r'Skip to main content', flags=re.IGNORECASE),
    re.compile(r'The Keyword', flags=re.IGNORECASE),
    re.compile(r'Share Twitter Facebook LinkedIn Mail Copy link', flags=re.IGNORECASE),
    re.compile(r'Home Product news', flags=re.IGNORECASE),
    re.compile(r'Product news', flags=re.IGNORECASE),
    re.compile(r'window\.[A-Z_]+', flags=re.IGNORECASE),
    re.compile(r'const \w+', flags=re.IGNORECASE),
    re.compile(r'document\.', flags=re.IGNORECASE),
    re.compile(r'"@context"', flags=re.IGNORECASE),
    re.compile(r'licenseKey:', flags=re.IGNORECASE),
    re.compile(r'applicationID:', flags=re.IGNORECASE),
    re.compile(r'browserID:', flags=re.IGNORECASE),
]

def extract_text(html: str) -> str:
    """Extract clean article text from HTML using bleach for sanitization."""
    if not html:
        return ''
    
    # Pre-clean: Remove script and style tags AND their content completely.
    # Bleach with strip=True removes the tags but leaves the content (e.g. <script>foo</script> -> foo).
    html = SCRIPT_REGEX.sub('', html)
    html = STYLE_REGEX.sub('', html)
    
    # Allowed tags and attributes for initial cleaning
    allowed_tags = ['p', 'div', 'br', 'li', 'h1', 'h2', 'h3', 'h4', 'h5', 'h6', 'article', 'section', 'b', 'i', 'u', 'em', 'strong', 'a']
    allowed_attrs = {'a': ['href', 'title']}
    
    # Sanitize HTML
    clean_html = bleach.clean(html, tags=allowed_tags, attributes=allowed_attrs, strip=True)
    
    # Remove navigation and UI elements (still useful to remove noise text)
    text = clean_html
    for pattern in NOISE_PATTERNS:
        text = pattern.sub('', text)
    
    # Replace block tags with newlines for text extraction
    text = BLOCK_TAGS_REGEX.sub('\n', text)

    # Remove remaining tags (strip=True removes tags, leaves content, but we are just removing allowed tags now)
    text = bleach.clean(text, tags=[], strip=True)

    # Clean up whitespace
    text = WHITESPACE_REGEX.sub(' ', text).strip()

    # Split into sentences and keep only meaningful ones
    sentences = SENTENCE_SPLIT_REGEX.split(text)
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
