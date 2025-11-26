# Changelog

All notable changes to this project will be documented in this file.

The format is based on "Keep a Changelog" and this project adheres to Semantic Versioning.

## [1.2.0] - 2025-11-26 - DUAL EMAIL SYSTEM 🚀

### 🎉 Major Features Added
- **Dual Email System**: Two complementary daily emails with specialized content
- **AI Tooling Roundup**: 12:00 PM daily - Developer tools, frameworks, coding assistance
- **AI Models & Releases**: 3:00 PM daily - New models, releases, enterprise features
- **Separate Configuration System**: Independent configs for each email type
- **Separate Cache Tracking**: Prevents duplicates within each email stream independently

### 📧 Email Specialization
- **AI Tooling (12 PM)**: OpenAI, Google Developers, GitHub, LangChain, AWS ML, HuggingFace
- **AI Models (3 PM)**: HuggingFace, OpenAI, Anthropic, Microsoft AI, ArXiv AI/CL, Google AI
- **Targeted Keywords**: Different keyword sets optimized for each content type
- **Optimized Sources**: 8 total sources across both emails for comprehensive coverage

### 🏗️ Architecture Enhancements
- **Config Selection**: `--config config` vs `--config config_models`
- **Dual Cache System**: `sent_articles.json` + `sent_articles_models.json`
- **Separate Logging**: `aimailer.log` + `models.log` for independent monitoring
- **Enhanced Pipeline**: Config-aware processing with separate tracking

### ⏰ Updated Scheduling
- **AI Tooling**: Daily at 12:00 PM (`0 12 * * *`)
- **AI Models**: Daily at 3:00 PM (`0 15 * * *`)
- **Queue Processing**: Every 15 minutes (unchanged)
- **Log Rotation**: Sundays at 2:00 AM (unchanged)

### 🛠️ New Components
- `config_models.py` - Configuration for AI Models & Releases email
- `run_models.sh` - Shell script for models email generation
- Enhanced `tracker.py` - Support for multiple cache files
- Enhanced `run.py` - Config selection and separate processing

### 📊 Performance Improvements
- **200+ articles processed daily** from 8 specialized sources
- **22 articles selected daily** (12 tooling + 10 models)
- **Separate duplicate tracking** prevents cross-contamination
- **Optimized source weighting** for each content type

### 🔧 Usage Updates
```bash
# Generate AI Tooling email
python src/run.py --config config --max-items 12

# Generate AI Models email  
python src/run.py --config config_models --max-items 10
```

### Changed
- **Email Count**: Single → Dual daily emails
- **Schedule**: 8 AM → 12 PM & 3 PM
- **Sources**: 6 → 8 total sources across both emails
- **Cache System**: Single → Dual independent tracking
- **Version**: 1.1.0 → 1.2.0

## [1.1.0] - 2025-11-26 - ENHANCED DAILY EDITION 🚀

### 🎉 Major Features Added
- **Daily Scheduling**: Changed from weekly to daily email delivery at 8:00 AM
- **Duplicate Article Prevention**: 30-day article tracking prevents repeat content
- **Multiple Recipients**: Support for sending to multiple email addresses individually
- **Article Cache Management**: Utilities to view and manage sent article history

### 📅 Schedule Changes
- **Old**: Weekly on Mondays at 8:00 AM (`0 8 * * 1`)
- **New**: Daily at 8:00 AM (`0 8 * * *`)
- **Processing**: Unchanged (every 15 minutes)

### 🚫 Duplicate Prevention System
- **Article Tracking**: JSON file-based cache (`sent_articles.json`)
- **30-Day Memory**: Automatically removes old entries after 30 days
- **Smart Filtering**: Filters out previously sent articles before processing
- **Cache Management**: `manage_cache.py` utility for viewing and clearing cache

### 👥 Multiple Recipients Support
- **Individual Delivery**: Each recipient gets their own email (not CC/BCC)
- **SQS Integration**: Creates separate queue messages for reliable delivery
- **Fault Tolerance**: Failed delivery to one recipient doesn't affect others
- **Configuration**: Simple list-based configuration in `config.py`

### 🏗️ Architecture Updates
- **New Component**: `tracker.py` for duplicate article prevention
- **Enhanced Pipeline**: Fetcher → **Tracker** → Extractor → Summarizer → Selector → Composer → SQS → SMTP
- **Cache Management**: Automatic cleanup and maintenance utilities

### Changed
- **Email Subject**: "Weekly AI Tooling Roundup" → "Daily AI Tooling Roundup"
- **Frequency**: Weekly → Daily
- **Recipients**: Single → Multiple support
- **Version**: 1.0.0 → 1.1.0

## [1.0.0] - 2025-11-26 - PRODUCTION RELEASE 🚀

### 🎉 Major Features Added
- **Complete RSS Pipeline**: Implemented full RSS fetching from 6 major AI/ML sources
- **AI-Powered Summarization**: Ollama integration with OpenAI fallback for article summaries
- **Source Diversity Algorithm**: Round-robin selection ensuring balanced content from all sources
- **Clean Text Extraction**: Advanced HTML cleaning filtering JavaScript/JSON noise
- **AWS SQS Integration**: Reliable email queuing and delivery system
- **Gmail SMTP Delivery**: Production email sending via Gmail SMTP
- **Automated Scheduling**: Cron-based weekly generation and continuous processing

### 📊 Content Sources Implemented
- OpenAI Blog RSS
- Google Developers Blog RSS
- GitHub Blog RSS
- HuggingFace Blog RSS
- AWS ML Blog RSS
- LangChain Blog RSS

### 🏗️ Architecture Completed
- **Fetcher Module**: RSS feed processing with feedparser
- **Extractor Module**: Clean text extraction from HTML
- **Summarizer Module**: LLM-powered article summarization
- **Selector Module**: Source diversity and ranking algorithms
- **Composer Module**: HTML email template generation
- **Sender Module**: AWS SQS queuing and SMTP delivery
- **Processor Module**: Queue processing and email sending

### Changed
- **Schedule**: Updated from Friday 9 AM to Monday 8 AM
- **Sources**: Expanded from 4 to 6 diverse AI/ML sources
- **Version**: Bumped from 0.1.0 to 1.0.0 (production ready)

## [0.1.0] - 2025-11-26
### Added
- Initial project scaffold and planning documents:
  - `BRIEF.md` — project brief and sample HTML email content
  - `SOURCES.md` — curated sources and pipeline outline
  - `PLAN.md` — project plan and pipeline overview
  - `TODO.md` — task list with current statuses
  - `project.json` — machine-friendly project manifest
  - `CHANGELOG.md` — this file

### Notes
- First commit captures planning and manifest creation
- Established development roadmap and technical requirements

---

**Status**: ✅ Production Ready | **Next Release**: TBD (maintenance and enhancements)
