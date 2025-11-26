# TODO — Weekly AI Tooling Roundup

Generated: 2025-11-26

- [in_progress] (high) 1 — Design pipeline & config (sources, schedule, creds)
- [pending] (high) 2 — Implement fetchers (RSS, APIs, Perplexica, SEARXNG)
- [pending] (high) 3 — Extract article text & summarize with LLM (2–3 sentences + why devs care)
- [pending] (medium) 4 — Dedupe, tag, score and select top ~12
- [pending] (medium) 5 — Compose HTML email template and test rendering
- [pending] (high) 6 — Send email via SMTP/Outlook/Gmail and schedule with cron
- [pending] (low) 7 — Add logging, monitoring, unsubscribe handling, and docs

Notes:
- Local search endpoints: `http://10.0.10.46:3030/discover` (Perplexica), `http://10.0.10.46:4040` (SEARXNG).
- Recipient: `stephen.z.phillips@sparktsl.com` (from brief).
- Suggested schedule: weekly Friday 09:00.

Next immediate steps:
1. Confirm LLM provider and email-sending method.
2. Create configuration file and skeleton fetcher module.
3. Implement extraction + LLM summarizer and test on a few sample articles.

---
To mark items completed, update this file or tell me which items to advance and I will edit it.