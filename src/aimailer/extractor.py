import re


def extract_text(html: str) -> str:
    """Extract clean article text from HTML, filtering out code and structured data."""
    if not html:
        return ''
    
    # Remove script tags and their content
    html = re.sub(r'<script[^>]*>.*?</script>', '', html, flags=re.DOTALL | re.IGNORECASE)
    
    # Remove style tags and their content
    html = re.sub(r'<style[^>]*>.*?</style>', '', html, flags=re.DOTALL | re.IGNORECASE)
    
    # Remove JSON-LD structured data
    html = re.sub(r'{\s*"@context"[^}]*}[^}]*}', '', html, flags=re.DOTALL)
    
    # Remove common code patterns
    html = re.sub(r'window\.[A-Z_]+[^;]*;', '', html)
    html = re.sub(r'const\s+\w+[^;]*;', '', html)
    html = re.sub(r'document\.[^;]*;', '', html)
    
    # Remove navigation and UI elements
    html = re.sub(r'Skip to main content', '', html, flags=re.IGNORECASE)
    html = re.sub(r'The Keyword', '', html, flags=re.IGNORECASE)
    html = re.sub(r'Share Twitter Facebook LinkedIn Mail Copy link', '', html, flags=re.IGNORECASE)
    html = re.sub(r'Home Product news', '', html, flags=re.IGNORECASE)
    
    # Replace common block tags with newlines
    html = re.sub(r'</?(p|div|br|li|h[1-6]|article|section)[^>]*>', '\n', html, flags=re.IGNORECASE)
    
    # Remove remaining tags
    text = re.sub(r'<[^>]+>', '', html)
    
    # Clean up whitespace
    text = re.sub(r'\s+', ' ', text).strip()
    
    # Remove common noise patterns
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
    
    for pattern in noise_patterns:
        text = re.sub(pattern, '', text, flags=re.IGNORECASE)
    
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
