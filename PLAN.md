# Weekly AI Tooling Roundup — Plan

## Goal
Deliver a weekly, agentic AI-powered email that summarizes ~12 recent articles about AI tools, agentic systems, and model releases relevant to an AI developer working on company tools and systems (recipient: stephen.z.phillips@sparktsl.com).

## Scope
- Focus: agentic/browser agents, MCP, CLI pair-programming tools, model releases, multimodal/image model updates, and devtooling that impacts engineering workflows.
- Example topics: Comet Browser, OpenAI Operator, BrowserOS (MCP), OpenCode, Amazon Q, Gemini CLI, GPT-5.1, Nano Banana Pro, Opus/Claude.
- Use local search tools `Perplexica` (`http://10.0.10.46:3030/discover`) and `SEARXNG` (`http://10.0.10.46:4040`) where helpful.

## Pipeline Overview
1. Fetch sources (RSS, APIs, web search via Perplexica/SEARXNG, GitHub/Product Hunt/Hacker News where applicable).
2. Normalize items to common schema: `{title, url, source, date, raw_text/snippet}`.
3. Extract article text (Readability/Mercury-like extraction) to minimize tokens.
4. Summarize with LLM: produce a 2–3 sentence summary + 1-sentence "why devs should care" + tags + confidence score.
5. Dedupe (URL normalization, fuzzy title match) and keep newest.
6. Score & rank by recency, keyword match, and source weight (official > curated > social).
7. Select top ~12 items.
8. Compose HTML email (use provided sample in `BRIEF.md`) and plain-text fallback.
9. Send email via chosen delivery method (SMTP/Gmail/Outlook) and schedule with cron.
10. Log events, monitor runs, and expose unsubscribe handling (mailto) per sample.

## Ranking & Tagging
- Keywords to seed ranking: `mcp`, `model context protocol`, `agent`, `operator`, `browser`, `comet`, `cli`, `terminal`, `coding assistant`, `pair programming`, `opencode`, `amazon q`, `gemini cli`, `anthropic`, `opus`, `gpt-5.1`, `gemini 3`, `multimodal`, `image model`.
- Scoring factors: recency (time decay), keyword match (presence/weight), source weight (official release blogs > curated newsletters > social posts), and LLM-provided confidence.

## LLM & Sending Options (decisions required)
- LLM choices: OpenAI, Anthropic, Google (Gemini), or local models. Tradeoffs: quality vs cost vs data locality.
- Delivery choices: SMTP (company SMTP credentials), Gmail API/SMTP, or Outlook/Microsoft Graph. Will need credentials or API tokens for chosen method.

## Schedule
- Default: weekly, Friday 09:00 local time (adjustable).

## Deliverables
- Working script (Python/Node) or n8n workflow that fetches → summarizes → sends.
- HTML email template using the sample in `BRIEF.md`.
- Config file for sources, credentials, schedule, and keywords.
- Basic logging and retry behavior.

## Next Actions / Questions
- Confirm LLM provider and provide API key access method (env vars preferred).
- Confirm email sending method and provide SMTP/API credentials (or confirm you want placeholder config).
- Confirm preferred schedule and whether to include external sources that require auth (e.g., Product Hunt API).


---
Generated from `BRIEF.md` and `SOURCES.md` on 2025-11-26.