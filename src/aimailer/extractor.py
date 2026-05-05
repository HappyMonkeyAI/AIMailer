import re
from bs4 import BeautifulSoup


def extract_text(html: str) -> str:
    """Extract clean article text from HTML, targeting main content and filtering noise."""
    if not html:
        return ''
    
    soup = BeautifulSoup(html, 'html.parser')
    
    # Remove script, style, nav, footer, and sidebar elements
    for element in soup(['script', 'style', 'nav', 'footer', 'aside', 'header']):
        element.decompose()

    # Common UI/Noise classes and IDs to remove
    noise_selectors = [
        '.wp-block-techcrunch-menu-utility',
        '.wp-block-techcrunch-site-search',
        '.strictly-vc-banner',
        '.ad-unit',
        '.social-share',
        '#menu-main-menu',
        '.nav-menu'
    ]
    for selector in noise_selectors:
        for element in soup.select(selector):
            element.decompose()

    # Try to find the main content container
    content_container = None
    priority_selectors = [
        'main',
        'article',
        '.entry-content',
        '.article-content',
        '.post-content',
        '.content'
    ]
    
    for selector in priority_selectors:
        found = soup.select_one(selector)
        if found:
            # Check if it has enough text to be the article
            if len(found.get_text(strip=True)) > 500:
                content_container = found
                break
    
    if not content_container:
        content_container = soup.body if soup.body else soup

    # Get text from paragraphs to preserve structure
    paragraphs = content_container.find_all(['p', 'h1', 'h2', 'h3', 'h4', 'h5', 'h6', 'li'])
    lines = []
    for p in paragraphs:
        text = p.get_text(separator=' ', strip=True)
        if text:
            # Basic noise filtering at sentence level
            if any(noise in text.lower() for noise in [
                'tickets are going fast', 
                'register now', 
                'skip to main content',
                'view bio',
                'follow us'
            ]):
                continue
            lines.append(text)

    # Join and clean up
    text = ' '.join(lines)
    text = re.sub(r'\s+', ' ', text).strip()
    
    # Split into sentences and keep only meaningful ones
    sentences = re.split(r'(?<=[.!?])\s+', text)
    clean_sentences = []
    
    for sentence in sentences:
        sentence = sentence.strip()
        if (len(sentence) > 30 and  # Increased minimum length
            not sentence.startswith('{') and
            not sentence.startswith('window') and
            not sentence.startswith('const') and
            not sentence.startswith('document') and
            len([c for c in sentence if c.isalpha()]) > len(sentence) * 0.7):
            clean_sentences.append(sentence)
    
    return '. '.join(clean_sentences[:15])  # Max 15 sentences for better context
