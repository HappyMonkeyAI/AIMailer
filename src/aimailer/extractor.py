import re


def extract_text(html: str) -> str:
    """Very small HTML-to-text extractor that removes tags and preserves paragraphs.
    This is intentionally simple to avoid external runtime dependencies.
    """
    if not html:
        return ''
    # Replace common block tags with newlines
    html = re.sub(r'</?(p|div|br|li|h[1-6])[^>]*>', '\n', html, flags=re.IGNORECASE)
    # Remove remaining tags
    text = re.sub(r'<[^>]+>', '', html)
    # Collapse whitespace
    text = re.sub(r'\s+', ' ', text).strip()
    return text
