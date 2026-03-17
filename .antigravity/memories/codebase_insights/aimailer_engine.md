# Codebase Insight: AIMailer Core Engine

## Overview
The core engine follows a modular pipeline designed for automated AI-content curation and delivery.

## Key Modules
- **Fetcher (`fetchers.py`)**: Handles RSS feed processing using `feedparser`.
- **Extractor (`extractor.py`)**: Sanitizes HTML and extracts readable text, filtering out JS/JSON noise.
- **Summarizer (`summarizer.py`)**: Integrates with local Ollama (primary) and OpenAI (fallback) for multi-stage summarization.
- **Selector (`selector.py`)**: Implements a round-robin source diversity algorithm to ensure balanced content.
- **Tracker (`tracker.py`)**: Manages de-duplication with a 30-day "memory" using JSON-based persistent storage.

## Hidden Knowledge
- **Dual Cache**: Content is split between `sent_articles.json` (Tooling) and `sent_articles_models.json` (Models) to allow independent stream scaling.
- **Ollama Fallback**: If Ollama timeouts or fails, the system automatically falls back to OpenAI to ensure daily delivery continuity.
- **Keyword Weights**: Sources are weighted based on content-specific keywords defined in `project.json`.
