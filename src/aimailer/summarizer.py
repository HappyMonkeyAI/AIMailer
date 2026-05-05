import os
import requests
from typing import Dict
from dotenv import load_dotenv

load_dotenv("/var/www/html/AIMailer/.env")

API_KEY = os.environ.get("OPENAI_API_KEY")
OLLAMA_URL = os.environ.get("OLLAMA_URL", "http://localhost:11434")
OLLAMA_MODEL = os.environ.get("OLLAMA_MODEL", "gemini-1.5-flash")
BRIDGE_AUTH_TOKEN = os.environ.get(
    "BRIDGE_AUTH_TOKEN", os.environ.get("OLLAMA_AUTH", "")
)

import re


def extract_json(text: str) -> Optional[Dict]:
    """Robustly extract the first JSON object found in text."""
    try:
        # Try direct load first
        return json.loads(text)
    except json.JSONDecodeError:
        pass

    # Hunt for the first { and last }
    start = text.find('{')
    end = text.rfind('}')
    if start != -1 and end != -1 and end > start:
        json_str = text[start:end+1]
        try:
            return json.loads(json_str)
        except json.JSONDecodeError:
            # Try cleaning common hallucinations like trailing commas
            # or missing quotes around keys if necessary, but keep it simple first
            pass
    return None


def summarize_text(text: str) -> Dict:
    if not text:
        return {"summary": "", "why_dev_care": "", "tags": [], "confidence": 0.0}
    
    # Build a concise prompt requesting summary + why devs care + tags
    prompt = (
        "TASK: Summarize the article provided below in 2-3 concise sentences. Focus on the core facts. "
        "Then provide one short sentence explaining why a software developer building AI tools should care about this. "
        "Finally, return 2-3 short tags separated by commas. "
        "IMPORTANT: Your response MUST contain a JSON object with these keys: 'summary', 'why', 'tags'. "
        "The JSON should be the primary output."
        "\n\nARTICLE:\n" + text[:10000]
    )
    # Try Ollama local model first
    ollama_raw = call_ollama(prompt, max_tokens=800)
    
    # Extract JSON object
    obj = extract_json(ollama_raw)
    
    if obj:
        # Extract fields with mapping for variations
        summary = obj.get('summary', '')
        why = obj.get('why', obj.get('why_dev_care', ''))
        tags_raw = obj.get('tags', '')
        if isinstance(tags_raw, list):
            tags = [str(t).strip() for t in tags_raw if str(t).strip()]
        else:
            tags = [t.strip() for t in str(tags_raw).split(',') if t.strip()]

        # Basic quality check: if summary is too short or just echoes article start, mark low confidence
        confidence = 0.95
        if len(summary) < 40 or summary.lower().strip().startswith('tickets are going fast'):
            confidence = 0.4

        return {
            'summary': summary,
            'why_dev_care': why,
            'tags': tags,
            'confidence': confidence
        }

    # Fallback extraction if no JSON found
    lines = [l.strip() for l in ollama_raw.split('\n') if l.strip()]
    summary = ""
    for line in lines:
        if not line.startswith('{') and len(line) > 50:
            summary = line[:500]
            break
    
    if not summary or any(n in summary.lower() for n in ['tickets are going fast', 'search submit', 'logo']):
        summary = "Article summary could not be extracted cleanly."
        confidence = 0.1
    else:
        confidence = 0.6
    
    return {'summary': summary, 'why_dev_care': '', 'tags': [], 'confidence': confidence}

    # If no Ollama result, fallback to stub or OpenAI if key present
    if API_KEY:
        # TODO: implement OpenAI call
        return {
            "summary": text.strip()[:300],
            "why_dev_care": "LLM placeholder",
            "tags": [],
            "confidence": 0.6,
        }
    # Fallback stub
    summary = text.strip().replace("
", " ")
    if len(summary) > 280:
        summary = summary[:277].rsplit(" ", 1)[0] + "..."
    return {
        "summary": summary,
        "why_dev_care": "Potentially relevant AI tooling update — review for integration potential.",
        "tags": [],
        "confidence": 0.1,
    }