1. Official model/tool release channels (highest signal)

These are where new capabilities actually land first, with real specs and examples.

OpenAI

OpenAI Blog / Research / Release notes (models, tools, APIs)

OpenAI Developer Forum (practical gotchas + rollouts)

OpenAI GitHub org (SDK updates, examples, MCP-ish integrations)

Anthropic

Anthropic News + Release posts (Claude, Opus/Sonnet updates)

Anthropic Docs changelog + Claude Code announcements

Google / DeepMind

Google AI Blog / DeepMind blog (Gemini, Nano Banana, agentic tools)

Gemini API changelog + model cards

Vertex AI & Google Cloud blog (enterprise model rollouts, Gemini CLI)

Amazon / AWS

AWS ML Blog + “What’s New in AI/ML”

Amazon Q Developer / CodeWhisperer updates

Microsoft

Azure AI Blog & “AI Foundry” updates

GitHub Copilot changelog + VS Code release notes

2. AI tooling & dev-tools newsletters (curated, weekly friendly)

Perfect for a weekly roundup because they already filter noise.

Ben’s Bites (daily AI product + tooling launches)

The Rundown AI (high-level but fast on new tools)

Import AI (Jack Clark) (slower cadence, deep signal)

Latent Space (builders + agents + toolchains)

TLDR AI (quick scan, good for rounding out)

This Week in AI Engineering (practical, dev-focused)

Hacker Newsletter / Pointer.io (software-dev angle, sometimes AI)

3. “Frontier dev” communities & launch surfaces (early warnings)

Where Comet-style things show up before blogs catch up.

Hacker News (esp. “Show HN” + comments)

Product Hunt (AI devtools category)

GitHub Trending

Topics: ai-agent, mcp, llm-tools, coding-assistant, cli, browser-automation

Reddit

r/LocalLLaMA

r/singularity (some hype, but early)

r/MachineLearning (papers + real changes)

r/ChatGPTCoding / r/ClaudeAI / r/Bard / r/OpenAI

X / Twitter lists (if you can tolerate it)

Make a private list of model labs + devtool founders.

4. Research & benchmark feeds (to catch model jumps)

Useful for “is this actually better?” and tooling-model fit.

arXiv

cs.AI, cs.CL, cs.LG, cs.SE (software eng)

Use arXiv RSS with keyword filters like “agent”, “tool use”, “browser”, “code generation”, “MCP”.

Papers with Code – Trending

SWE-bench / HELM / LMSYS Arena updates

Vellum / Artificial Analysis (practical eval writeups & cost/perf)

5. MCP / agentic ecosystem sources (your specific niche)

Since you explicitly care about MCP + browsers + agents:

Model Context Protocol (MCP) GitHub + spec repos

Awesome-MCP lists on GitHub

Cursor / Windsurf / Zed / VS Code AI extension changelogs

LangChain / LlamaIndex / Vercel AI SDK / PydanticAI blogs

These frameworks often add MCP or agent runtime support quickly.

n8n community templates & forum (people ship AI automations fast)

6. A few “always good” long-form sources

Slower, more contextual, great for weekly wrapups.

The Information / WSJ / FT tech (if you have access)

The Verge / Ars Technica / TechCrunch AI

SemiAnalysis / Stratechery (compute + model economics)

Noahpinion / Zvi / Dwarkesh (varies, but deep when relevant)

How to turn this into an n8n weekly email (practical outline)

Goal: fetch → dedupe → summarize → rank → email.

Pipeline idea

Cron node

Weekly, e.g., Friday 9am.

Fetch sources

RSS Read nodes for blogs/newsletters/arXiv.

HTTP Request nodes for:

GitHub search/trending (via GitHub API)

Product Hunt (API)

Hacker News (Algolia HN API)

Optional: X/Twitter via your preferred scraper/API.

Normalize items

Map to a common schema:
{title, url, source, date, raw_text/snippet}

Dedupe

Use a Function node:

normalize URLs (utm_ stripping)

fuzzy title match

keep newest

Enrich / extract

If RSS doesn’t include content:

run a Webpage Extract node (Mercury Parser, Readability, Jina AI reader, etc.)

LLM summarize

Send each article to your preferred model.

Ask for:

2–3 sentence summary

why devs should care

tags (e.g., browser-agent, mcp, cli-copilot, model-release)

Keep token usage low by summarizing only extracted main text.

Rank/select top ~12

Score by:

recency

keyword match to your interest list

source weight (official > curated > social)

Another Function node can do this.

Compose HTML email

Use an HTML Template node:

Title

bullet list with summary + “Read more” link

section headers by tag

Send

SMTP node or Outlook/Gmail node depending on your setup.

Keyword seed list (for ranking)

Start with:
mcp, model context protocol, agent, operator, browser, comet, dia, cli, terminal, coding assistant, pair programming, copilot, opencode, amazon q, gemini cli, cursor, windsurf, zed, anthropic, opus, sonnet, gpt-5.1, gemini 3, multimodal, image model