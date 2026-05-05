# AIMailer - Project Instructions & Workflows

This document follows the Antigravity Agents Prompt Protocol (A2P2). It provides high-level architectural guidance and repo-wide workflows.

## 🏗️ Architecture

### Dual-Layer Design
AIMailer consists of two primary layers:
1.  **Core Engine (`src/aimailer/`)**: A framework-agnostic Python package for fetching, summarizing, and sending emails.
2.  **Web Control Panel (`web/`)**: A Django 4.2 application for dynamic configuration, subscriber management, and task scheduling.

**Key Rule**: The Core Engine MUST remain decoupled from Django. Use adapters (like `NewsletterConfigAdapter` in `web/newsletters/tasks.py`) to bridge the two.

### Security Model
- **Credential Protection**: All sensitive SMTP passwords in the database MUST be encrypted using Fernet (via the `SMTPConfig` model).
- **SSRF Protection**: All data fetching MUST pass through the `is_safe_url` validator in `src/aimailer/fetchers.py`.
- **Header Injection**: User-provided sender names MUST be sanitized in `src/aimailer/sender.py`.

## 🛠️ Workflows

### Testing
- Core engine tests are located in `tests/`. Run with `PYTHONPATH=src pytest tests/`.
- Django web tests are located in `web/*/tests/`. Run with `python web/manage.py test`.

### Newsletter Processing
Processing is handled by Celery tasks in `web/newsletters/tasks.py`. 
- **Dry Run**: Can be toggled via `config_json` in the `NewsletterConfig` model.
- **LLM**: Primary summarization uses Ollama; OpenAI is reserved for fallback.

## 📚 Long-Term Memory (LTM)
Project insights and historical decisions are stored in `.antigravity/memories/`.
- `architectural_decisions/`: ADRs like the CLI-to-Django migration.
- `codebase_insights/`: Detailed notes on specific subsystems.
- `patterns_and_lessons/`: Recurring coding patterns and security lessons.
