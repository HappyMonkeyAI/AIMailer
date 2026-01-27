# Code Review: AIMailer

## 1. Security Issues

### 🔴 Critical Issues

#### 1. Insecure HTML Sanitization (Regex-based)
- **File:** `src/aimailer/extractor.py`
- **Lines:** 5-75 (`extract_text` function)
- **Problem:** The code uses regular expressions to sanitize HTML. This is fundamentally insecure and prone to evasion (e.g., nested tags, malformed HTML, event handlers). It fails to properly protect against XSS if the output is rendered in a web context or an email client that executes JS (though less common in email, it's bad practice). It also risks stripping legitimate content or leaving malicious artifacts.
- **Suggested Solution:** Use a dedicated library like `bleach` or `BeautifulSoup`'s cleaning capabilities (though `bleach` is preferred for sanitization).

```python
import bleach

def extract_text(html: str) -> str:
    if not html:
        return ''

    # Allow only safe tags and attributes
    allowed_tags = ['p', 'b', 'i', 'u', 'em', 'strong', 'a']
    allowed_attrs = {'a': ['href', 'title']}

    clean_html = bleach.clean(html, tags=allowed_tags, attributes=allowed_attrs, strip=True)

    # Further text processing...
    return clean_html
```
- **Rationale:** Prevents XSS vulnerabilities and ensures more robust parsing of malformed HTML.

#### 2. Hardcoded Secrets and Paths
- **File:** `src/aimailer/config.py`
- **Lines:** 14 (`CACHE_FILE = '/var/www/html/happymonkey.ai/AIMailer/sent_articles.json'`)
- **Problem:** Hardcoding absolute paths restricts the application to a specific environment and file structure. It also poses a security risk if the path is in a web-accessible directory (`/var/www/html`), potentially exposing the cache file to the public internet.
- **Suggested Solution:** Use environment variables or relative paths.

```python
import os
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent.parent
CACHE_FILE = os.environ.get('CACHE_FILE', str(BASE_DIR / 'sent_articles.json'))
```
- **Rationale:** Improves portability and security by decoupling configuration from code and keeping data files out of web roots.

### 🟡 Suggestions

#### 1. Broad Exception Handling
- **File:** `src/aimailer/fetchers.py`, `src/aimailer/summarizer.py`
- **Lines:** 11, 24 (fetchers), 28, 51 (summarizer)
- **Problem:** Catching `Exception` broadly (`except Exception:`) hides specific errors (like `KeyboardInterrupt` or `MemoryError`) and makes debugging difficult. It swallows connection errors silently.
- **Suggested Solution:** Catch specific exceptions (e.g., `requests.RequestException`, `feedparser.FeedParserDict`).

```python
import requests

def fetch_http(url: str, timeout: int = 10) -> Optional[str]:
    try:
        r = requests.get(url, timeout=timeout)
        r.raise_for_status()
        return r.text
    except requests.RequestException as e:
        # Log the error properly
        print(f"Error fetching {url}: {e}")
        return None
```
- **Rationale:** Allows for proper error handling and logging, preventing silent failures.

## 2. Performance & Efficiency

### 🟡 Suggestions

#### 1. Sequential AI Summarization
- **File:** `src/aimailer/summarizer.py`
- **Lines:** 33 (`summarize_text`)
- **Problem:** The summarization process likely iterates through articles one by one. Calling an external LLM (Ollama or OpenAI) is blocking and high-latency. Processing 100+ articles sequentially will take a significant amount of time.
- **Suggested Solution:** Use `asyncio` or `concurrent.futures.ThreadPoolExecutor` to parallelize summarization requests.

```python
import concurrent.futures

def summarize_batch(articles):
    with concurrent.futures.ThreadPoolExecutor(max_workers=5) as executor:
        future_to_article = {executor.submit(summarize_text, a['text']): a for a in articles}
        for future in concurrent.futures.as_completed(future_to_article):
            # Process results
            pass
```
- **Rationale:** Drastically reduces total processing time for batch jobs.

## 3. Code Quality

### 🟡 Suggestions

#### 1. Code Duplication in Cache Management
- **File:** `src/aimailer/tracker.py`
- **Lines:** 19-30 (cleaning in load), 53-60 (cleaning in save)
- **Problem:** The logic for cleaning old entries is duplicated in `load_sent_articles` and `save_sent_articles`.
- **Suggested Solution:** Extract the cleaning logic into a private helper function `_clean_old_entries(data: dict) -> dict`.
- **Rationale:** Adheres to DRY (Don't Repeat Yourself) principle, reducing maintenance burden.

#### 2. Fragile Regex for Text Cleaning
- **File:** `src/aimailer/extractor.py`
- **Lines:** 54-68 (noise patterns)
- **Problem:** The list of `noise_patterns` is specific to current sources. If sources change layout, this will break. The logic is also brittle (e.g., hardcoded `len(sentence) > 20`).
- **Suggested Solution:** Use a library like `readability-lxml` or `trafilatura` which are designed to extract main content from web pages.
- **Rationale:** These libraries are more robust and maintained than custom regex heuristics.

## 4. Architecture & Design

### ✅ Good Practices
- **Pipeline Structure:** The separation of Fetch -> Extract -> Summarize -> Select -> Compose -> Send in `src/aimailer/` is a solid architectural choice. It allows for easy testing and replacement of individual components.
- **Django Settings:** Using `environ` for sensitive settings in `web/config/settings.py` is a good practice (though defaults should be safe).

### 🟡 Suggestions

#### 1. Dependency Injection for Configuration
- **File:** `src/aimailer/config.py` is imported directly.
- **Problem:** This makes it hard to test components with different configurations without mocking.
- **Suggested Solution:** Pass a configuration object to functions instead of relying on global module-level variables.

## 5. Testing & Documentation

### 🔴 Critical Issues

#### 1. Lack of Unit Tests for Core Logic
- **Scope:** `src/aimailer/`
- **Problem:** There are no visible unit tests for the core logic (extractor, selector, summarizer). The `tests/` directory exists but content is unknown/unreferenced in the plan.
- **Suggested Solution:** specific tests for `extractor.py` (with sample HTML), `selector.py` (ensuring diversity logic works), and `tracker.py`.
- **Rationale:** Ensures reliability and prevents regressions during refactoring.

### ✅ Good Practices
- **Docstrings:** Most functions have clear docstrings explaining their purpose.
