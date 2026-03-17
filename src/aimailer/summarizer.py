import os
import requests
from typing import Dict

API_KEY = os.environ.get('OPENAI_API_KEY')
OLLAMA_URL = os.environ.get('OLLAMA_URL', 'http://localhost:11434')
OLLAMA_MODEL = os.environ.get('OLLAMA_MODEL', 'qwen2.5:7b-instruct-q4_K_M')

import re


def clean_thought_blocks(text: str) -> str:
    """
    Remove common 'thinking' or 'reasoning' blocks from LLM output.
    Supports <thought>, [[[thought]]], <reasoning>, etc.
    """
    if not text:
        return ""
    # Standard XML-like tags
    text = re.sub(r'<thought>.*?</thought>', '', text, flags=re.DOTALL | re.IGNORECASE)
    text = re.sub(r'<reasoning>.*?</reasoning>', '', text, flags=re.DOTALL | re.IGNORECASE)
    # Double/Triple brackets common in some fine-tuned models
    text = re.sub(r'\[\[\[?thought\]\]\].*?\[\[\[?/thought\]\]\]', '', text, flags=re.DOTALL | re.IGNORECASE)
    # DeepSeek/Open-style <think> tags
    text = re.sub(r'<think>.*?</think>', '', text, flags=re.DOTALL | re.IGNORECASE)
    
    return text.strip()


def call_ollama(prompt: str, max_tokens: int = 512) -> str:
    try:
        url = OLLAMA_URL.rstrip('/') + '/api/generate'
        payload = {
            'model': OLLAMA_MODEL,
            'prompt': prompt,
            'max_tokens': max_tokens,
            'temperature': 0.2,
            'stream': False,
        }
        resp = requests.post(url, json=payload, timeout=120)
        resp.raise_for_status()
        data = resp.json()
        # Ollama responses vary; try to extract common fields
        if isinstance(data, dict) and 'text' in data:
            return data['text']
        # Ollama standard field
        if isinstance(data, dict) and 'response' in data:
            return data['response']
        # Some Ollama setups stream or return 'completion'
        if isinstance(data, dict) and 'completion' in data:
            return data['completion']
        # Fallback: stringify
        return str(data)
    except requests.RequestException as e:
        print(f"Ollama API error: {e}")
        return ''
    except Exception as e:
        print(f"Unexpected error calling Ollama: {e}")
        return ''


def summarize_text(text: str) -> Dict:
    if not text:
        return {'summary': '', 'why_dev_care': '', 'tags': [], 'confidence': 0.0}
    # Build a concise prompt requesting summary + why devs care + tags
    prompt = (
        "Summarize the following article in 2-3 short sentences. Then provide one short sentence explaining why a software developer building AI tools should care. "
        "Finally, return 2-3 short tags separated by commas. Use JSON format with keys: summary, why, tags.\n\nARTICLE:\n" + text[:10000]
    )
    # Try Ollama local model first
    ollama_raw = call_ollama(prompt, max_tokens=600)
    ollama_out = clean_thought_blocks(ollama_raw)
    if ollama_out:
        # Try to parse JSON from model
        try:
            import json
            # Heuristic: find the first '{' and last '}' to extract JSON block
            # Heuristic: find the first '{' and last '}' to extract JSON block
            match = re.search(r'\{.*\}', ollama_out, re.DOTALL)
            if match:
                json_str = match.group(0)
                obj = json.loads(json_str)
            else:
                obj = json.loads(ollama_out)
            
            return {'summary': obj.get('summary',''), 'why_dev_care': obj.get('why',''), 'tags': [t.strip() for t in obj.get('tags','').split(',') if t.strip()], 'confidence': 0.9}
        except Exception:
            # If not JSON or fails parsing, heuristic fallback
            summary = ollama_out.strip().split('\n\n')[0][:600]
            return {'summary': summary, 'why_dev_care': '', 'tags': [], 'confidence': 0.7}

    # If no Ollama result, fallback to stub or OpenAI if key present
    if API_KEY:
        # TODO: implement OpenAI call
        return {'summary': text.strip()[:300], 'why_dev_care': 'LLM placeholder', 'tags': [], 'confidence': 0.6}
    # Fallback stub
    summary = text.strip().replace('\n', ' ')
    if len(summary) > 280:
        summary = summary[:277].rsplit(' ', 1)[0] + '...'
    return {'summary': summary, 'why_dev_care': 'Potentially relevant AI tooling update — review for integration potential.', 'tags': [], 'confidence': 0.1}
