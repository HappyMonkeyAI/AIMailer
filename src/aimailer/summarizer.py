import os
from typing import Dict

API_KEY = os.environ.get('OPENAI_API_KEY')


def summarize_text(text: str) -> Dict:
    """Return a dict with summary, why_dev_care, tags. Uses API if API_KEY present, otherwise stub.
    Keep summaries short (2-3 sentences) in the stub.
    """
    if not text:
        return {'summary': '', 'why_dev_care': '', 'tags': []}
    if API_KEY:
        # TODO: call an LLM provider here (OpenAI/Gemini/Anthropic) using the API key.
        # For now return a short slice as placeholder.
        return {'summary': text.strip().replace('\n', ' ')[:300], 'why_dev_care': 'LLM-generated summary placeholder', 'tags': []}
    # Fallback stub summarizer
    summary = text.strip().replace('\n', ' ')
    if len(summary) > 280:
        summary = summary[:277].rsplit(' ', 1)[0] + '...'
    return {'summary': summary, 'why_dev_care': 'Potentially relevant AI tooling update — review for integration potential.', 'tags': []}
