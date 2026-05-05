# AIMailer Project State & Improvement Report

## Executive Summary

AIMailer is an **AI-powered automated newsletter system** that fetches articles from RSS feeds, extracts content, generates LLM-powered summaries, scores/ranks them, and sends curated email roundups. Originally scoped as a weekly "AI Tooling Roundup" for a developer's work email, it has evolved (and stalled) into a multi-newsletter platform with a Django admin web panel.

**Overall status: 60-70% complete for its original purpose, 40% complete for its apparent later purpose.** The code is structurally sound but has gaps, inconsistencies, and has been inactive for ~4 months.

---

## Architecture Overview

```
src/ (CLI Pipeline)        web/ (Django Admin)
├── run.py        159 lines  ├── newsletters/     8.8KB models, 10.4KB tasks
├── aimailer/
│  ├── fetchers.py     69   ├── accounts/        (custom user + SMTPConfig)
│  ├── extractor.py    67   ├── public/          (views, models)
│  ├── summarizer.py  100   └── config/          (settings, celery, urls)
│  ├── selector.py    156   ─── staticfiles/       (Django admin CSS/JS)
│  ├── composer.py    16    ─── celerybeat-schedule
│  ├── sender.py     107   
│  ├── tracker.py    227   ─── migrations/ (6)
│  └── feed_cache.py  57
─── process_email_queue.py
```

**Total Python code: ~1,871 lines.** The Django web panel is ~60% of the codebase by file count, which is disproportionate for a system that started as a personal CLI script.

---

## Critical Issues (Fix These First)

### 1. Config file is wrong — project scope drift
`src/aimailer/config.py` is now configured for **"Crypto News"** (line 1-26), not the original AI Tooling Roundup:
- `EMAIL_TITLE = 'Crypto News'`
- `KEYWORDS = ['crypto', 'bitcoin', 'ethereum', ...]`
- `RECIPIENTS = ['info@happymonkey.ai']`
- 8 crypto RSS sources

**Impact:** The pipeline currently defaults to the crypto config. Either the original AI config was deleted or never re-added. Need to restore the AI tooling config (`config_models.py` is referenced but does not exist on disk).

### 2. Empty data file — broken pipeline path
`local_newsletters_data.json` is **0 bytes** and `local_newsletters_setup.json` points to a local article fetching path (`/home/stephen/Local Articles/Articles/` directory that likely doesn't exist on the server). The web panel's `fetch_local_articles()` will silently produce zero results.

### 3. Dead import in src/aimailer/summarizer.py
Line 5: `API_KEY=os.env...EY')` — this is a **truncated/broken string**. Even if you import the module, Python throws a syntax error at import time. The OpenAI fallback path is completely dead.

### 4. No active deployment / last code change was 4 months ago
The CHANGELOG claims "PRODUCTION COMPLETE" but the git log's most recent commit is from **March 18**. No active cron jobs have been running the pipeline. The TODO.md still shows tasks like "Implement unsubscribe handling" as unverified.

---

## Major Gaps

### 5. Composer outputs a bare-bones div (not the BRIEF.md template)
`src/aimailer/composer.py` is 16 lines that produce raw divs with inline styles. The BRIEF.md contains a polished, table-based, branded HTML email with header/body/footer styling. The composer does not use the BRIEF.md template at all — you'd need a full rewrite to match the intended email quality.

### 6. Key components have zero tests
- `composer.py` — 0 tests
- `sender.py` — 0 tests
- `fetchers.py` — 0 tests
- `extractor.py` — has `tests/test_extractor.py` (1,370 lines) — good
- `selector.py` — has `tests/test_selector.py` — good
- `tracker.py` — has `tests/test_tracker.py`, `test_tracker_db.py`, `test_tracker_migration.py` — good
- `summarizer.py` — has `tests/test_summarizer.py` — good

### 7. Email delivery defaults to dry_run=True
`sender.send_email()` has `dry_run=True` as default. The pipeline in `tasks.py` does pass `dry_run=config.config_json.get('dry_run', False)`, which means if a newsletter's `config_json.dry_run` is ever left unset or True, emails won't be sent. Not a bug per se, but a silent failure risk.

### 8. Perplexica/SEARXNG integration is best-effort with hardcoded fallbacks
Both default URLs (`localhost:3030`, `localhost:4040`) won't work unless those services are running locally. The `fetch_http()` calls on these return silently on failure. There's no visibility into "were these search sources contributing articles?" in the logs.

### 9. Docker Compose has placeholder passwords
`POSTGRES_PASSWORD=***` and `SECRET_KEY=django...-key` are not real secrets. The `.env` file also has no actual secrets populated — likely never was in production.

---

## Medium Priorities

### 10. LLM summarization quality depends on a small local model
The default model is `qwen2.5:7b-instruct-q4_K_M`. For generating high-quality, structured JSON summaries with "why devs care" and tags, this model is underpowered. The Ollama response parsing also uses a broad `{...}` regex heuristic with no JSON schema validation — malformed JSON silently falls back to a stub with `confidence: 0.1`.

### 11. Django admin panel is over-engineered for a personal tool
The web panel includes subscriber management, send history, email events, category system, logo/banner uploads, multi-newsletter configs, and a full NewsletterConfig model. For a personal AI tooling roundup, this is **massive over-engineering**. The original scope was a single recipient, single pipeline.

### 12. Thread safety in tracker module
`tracker.py` uses file-based cache with `threading.Lock(_MIGRATION_LOCK)` which is good, but the file-based `save_sent_articles()` does a read-then-write pattern without a file lock. If two pipeline runs execute simultaneously, one's writes could overwrite the other's data.

### 13. No error recovery or retry logic
If an RSS feed fails mid-run, the pipeline continues with missing sources. If a summarizer call fails for 5 items, those items get stubbed summaries with low confidence but are still included in the email. No exponential retry, no circuit breaker.

### 14. No monitoring, alerting, or analytics
Despite mentioning "AWS SQS integration" in the docs, the sender module only implements SMTP. The `boto3` dependency in `requirements.txt` is never used. There's no dashboard or log aggregation to track: "is the pipeline running? Did it send? What articles are trending?"

---

## Minor/Presentation Issues

### 15. CHANGELOG v1.2.0 claims "200+ articles processed daily, 22 selected" — unverified
120 days without a pipeline run means this performance claim is historical at best.

### 16. TODO.md marks ALL tasks as complete but they don't exist
The TODO has "Implement unsubscribe handling" with no actual unsubscribe endpoint, and "Deploy to server" with no server.

### 17. Code comments reference AWS SQS throughout but never use boto3
The sender module has SMTP only. The docs say "AWS SQS + Gmail SMTP" but the codebase is SMTP-only. This is documentation rot.

### 18. `local_newsletters_data.json` and `local_newsletters_setup.json` in root
These look like failed attempts to integrate a personal article reader. They should be cleaned up or moved to `web/` with a feature flag.

---

## Improvement Roadmap (Prioritized)

### Phase 1: Restore Core Functionality (1-2 days)
1. **Recreate the AI tooling config** — `src/aimailer/config.py` needs the original AI keywords, RSS sources, and recipient
2. **Create `config_models.py`** (already referenced but missing)
3. **Fix the broken `os.env...EY` import** in summarizer.py
4. **Populate `local_newsletters_data.json` or remove it** if it's dead code
5. **Test the pipeline end-to-end** with `--dry-run` and verify article count

### Phase 2: Reliability (2-3 days)
6. **Add email template rendering** — swap composer to use the BRIEF.md template
7. **Add retry logic** to fetchers with exponential backoff
8. **Make SEARXNG/Perplexica config-driven** with fallback detection
9. **Fix file cache lock** in tracker.py with proper file locking
10. **Add unit tests** for composer, sender, and fetchers (~300 lines)

### Phase 3: Quality of Life (3-5 days)
11. **Upgrade the LLM provider** — use a better model (GPT-4o-mini, Claude Haiku, or a larger Ollama model) for summary quality
12. **Add monitoring** — a simple health-check endpoint in Django that reports last run status, article counts, errors
13. **Add alerting** — email/Telegram notification on pipeline failure
14. **Clean up docs** — remove AWS SQS references, update TODO.md, fix CHANGELOG

### Phase 4: Architecture Decisions (Week 2+)
15. **Decision: web panel or not?** If this stays a personal tool, the Django panel is bloat. If it's a multi-user platform, invest in auth, RBAC, and tenant isolation.
16. **Database** — consider moving from SQLite to PostgreSQL (the Docker Compose already has PG)
17. **Logging** — structured logging with a log aggregation solution
18. **CI/CD** — add pre-commit hooks, test runs on PR, Docker build pipeline

---

## Bottom Line

The project has a **solid architectural foundation** (modular pipeline, separation of concerns, Docker setup) but has **stalled at "MVP-in-progress"**. The original AI tooling pipeline is broken due to the crypto config takeover, the broken import, and missing config files. The web panel is half-implemented. The most impactful next step is to restore the original AI pipeline, test it end-to-end, then decide whether to shrink it down to a lean CLI tool or invest in the multi-user web platform.
