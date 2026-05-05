# Architectural Decision: Native Deployment on GCP (No Docker)

## Status
**Active** (Migration completed 2026-03-17)

## Context
The GCP instance has 2 vCPU and limited RAM. Docker overhead was impractical.  
The system was migrated from a Docker Compose setup to a native deployment.

## Decision
Run all services natively:
- **Gunicorn** via `aimailer.service` (systemd) → serves Django on `127.0.0.1:8001`
- **Nginx** → reverse proxies to Gunicorn  
- **Cron** → replaces Celery Beat for scheduled email sends  
  ```
  0 12 * * *   cd ~/AIMailer && ~/AIMailer/venv/bin/python src/run.py
  0 15 * * *   cd ~/AIMailer && ~/AIMailer/venv/bin/python src/run.py
  ```
- **`run_aimailer.sh`** → canonical launcher (loads .env, activates venv, logs to `aimailer.log`)

## Tradeoffs
- **Pros**: No Docker overhead, full RAM available to app, simpler ops on small VMs.
- **Cons**: No container isolation; cron is less observable than Celery Beat.

## Hidden Knowledge
- **`src/aimailer/config.py` is NOT in the Docker image or git history** — it must be created manually on new deployments. Without it, all cron runs fail silently with `ModuleNotFoundError: No module named 'aimailer.config'`.
- The correct launcher is `run_aimailer.sh` NOT direct `python src/run.py` (the script loads .env and sets the working directory correctly).
- SMTP: SSL on port 465 via `198.54.120.137` (`info@happymonkey.ai`).
- Perplexica / SearxNG endpoints (`192.168.1.2`) are local network only — will timeout on GCP. These are gracefully skipped.
- `cryptopotato.com/feed/` returns malformed XML — also best-effort skipped.

## Post-Fix Verification
- First successful live email sent: **2026-03-18 17:58 UTC**
- 133 articles fetched, 12 selected, 1 email delivered to `info@happymonkey.ai`
