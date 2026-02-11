# AIMailer - Dual Daily AI Roundups

**Automated dual daily email system: AI Tooling (12 PM) + AI Models & Releases (3 PM)**

[![Status](https://img.shields.io/badge/Status-Production-green)](https://github.com/user/aimailer)
[![Version](https://img.shields.io/badge/Version-1.2.0-blue)](https://github.com/user/aimailer)
[![Python](https://img.shields.io/badge/Python-3.12+-blue)](https://python.org)

## 🎯 Overview

AIMailer is a production-ready system that delivers two complementary daily email roundups for AI developers:

- **12:00 PM**: AI Tooling Roundup - Developer tools, frameworks, coding assistance
- **3:00 PM**: AI Models & Releases - New models, releases, enterprise features

Each email processes 100+ articles from specialized sources and delivers 10-12 most relevant items with intelligent duplicate prevention.

## ✨ Features

- **🔄 Dual Email System**: Two specialized daily roundups with separate tracking
- **🤖 AI-Powered**: Ollama-based summarization with OpenAI fallback
- **📊 Source Diversity**: Round-robin selection ensures balanced content from all sources
- **🧹 Clean Extraction**: Advanced HTML cleaning removes JavaScript/JSON noise
- **📅 Scheduled**: Automated dual delivery at 12 PM and 3 PM daily
- **🚫 Duplicate Prevention**: 30-day article tracking per email type
- **👥 Multiple Recipients**: Support for multiple email addresses
- **🔍 Monitoring**: Comprehensive logging and error handling

## 📧 Email Types

### 🛠️ AI Tooling Roundup (12:00 PM)
**Focus**: Developer tools, frameworks, coding assistance, business tooling
- **Sources**: OpenAI Blog, Google Developers, GitHub Blog, LangChain, AWS ML, HuggingFace
- **Keywords**: mcp, agent, cli, tooling, frameworks, coding
- **Cache**: `sent_articles.json`

### 🤖 AI Models & Releases (3:00 PM)  
**Focus**: New models, releases, coding AI, enterprise features, major updates
- **Sources**: HuggingFace, OpenAI, Anthropic, Microsoft AI, ArXiv AI/CL, Google AI
- **Keywords**: model, release, GPT, Gemini, Claude, Opus, Grok, fine-tuning, enterprise
- **Cache**: `sent_articles_models.json`

## 🏗️ Architecture

```
Config Selection → RSS Feeds → Duplicate Filter → Content Fetcher → Text Extractor → 
AI Summarizer → Source Selector → Email Composer → SQS Queue → SMTP Sender → Gmail
```

### Components

- **Config** (`config.py` + `config_models.py`): Dual configuration system
- **Fetcher** (`fetchers.py`): RSS feed processing with feedparser
- **Tracker** (`tracker.py`): Separate duplicate prevention per email type
- **Extractor** (`extractor.py`): Clean text extraction from HTML
- **Summarizer** (`summarizer.py`): Ollama/OpenAI-powered summarization
- **Selector** (`selector.py`): Source diversity and ranking algorithms
- **Composer** (`composer.py`): HTML email template generation
- **Sender** (`sender.py`): AWS SQS queuing and SMTP delivery
- **Processor** (`process_email_queue.py`): Queue processing and email sending

## 🐳 Quick Start with Docker

The fastest way to get the AIMailer web control panel up and running is using Docker Compose.

```bash
# Clone the repository
git clone <repository>
cd AIMailer

# Start all services (Database, Redis, Web, Celery)
docker-compose up -d --build

# Create a superuser to access the admin panel
docker-compose exec web python manage.py createsuperuser
```

Once started, the services will be available at:
- **Web Admin**: [http://localhost:8001/admin](http://localhost:8001/admin)
- **Database**: Port 5432 (Internal)
- **Redis**: Port 6379 (Internal)

## 🚀 Manual Installation

### Prerequisites

- Python 3.12+
- AWS account with SQS access
- Gmail account with app password

### Installation

```bash
# Clone and setup
git clone <repository>
cd AIMailer
python -m venv venv
source venv/bin/activate
pip install -r requirements.txt

# Configure environment
cp .env.example .env
# Edit .env with your credentials
```

### Configuration

Update `.env` with your settings:

```bash
# LLM Configuration
OLLAMA_URL="https://ollama.wifispark.net"
OLLAMA_MODEL="qwen2.5:7b-instruct-q4_K_M"

# Email Configuration  
SMTP_HOST="smtp.gmail.com"
SMTP_PORT=587
SMTP_USER="your-email@gmail.com"
SMTP_PASS="your-16-char-app-password"

# AWS Configuration
SQS_QUEUE_URL="your-sqs-queue-url"
AWS_REGION="us-east-1"
```

### Multiple Recipients

Edit both `src/aimailer/config.py` and `src/aimailer/config_models.py`:
```python
RECIPIENTS = [
    'user1@example.com',
    'user2@example.com',
    'team@example.com',
]
```

### Usage

```bash
# Generate AI Tooling email
python src/run.py --config config --max-items 12

# Generate AI Models email
python src/run.py --config config_models --max-items 10

# Process email queue
./run_processor.sh

# Check logs
tail -f aimailer.log models.log processor.log

# Manage article caches
python manage_cache.py show    # View sent articles
python manage_cache.py clear   # Reset cache
```

## ⏰ Automated Scheduling

The system runs automatically via cron jobs:

```bash
# AI Tooling Roundup (12 PM daily)
0 12 * * * /var/www/html/happymonkey.ai/AIMailer/run_aimailer.sh

# AI Models & Releases (3 PM daily)
0 15 * * * /var/www/html/happymonkey.ai/AIMailer/run_models.sh

# Queue processing (every 15 minutes)
*/15 * * * * /var/www/html/happymonkey.ai/AIMailer/run_processor.sh >> /var/www/html/happymonkey.ai/AIMailer/processor.log 2>&1

# Log rotation (Sundays 2 AM)
0 2 * * 0 /var/www/html/happymonkey.ai/AIMailer/rotate_logs.sh >> /var/www/html/happymonkey.ai/AIMailer/rotation.log 2>&1
```

## 📁 Project Structure

```
AIMailer/
├── src/
│   ├── aimailer/
│   │   ├── config.py            # AI Tooling configuration
│   │   ├── config_models.py     # AI Models configuration
│   │   ├── fetchers.py          # RSS feed processing
│   │   ├── tracker.py           # Duplicate prevention
│   │   ├── extractor.py         # HTML text extraction
│   │   ├── summarizer.py        # AI summarization
│   │   ├── selector.py          # Content selection & diversity
│   │   ├── composer.py          # Email composition
│   │   └── sender.py            # SQS queuing & SMTP
│   ├── run.py                   # Main pipeline orchestrator
│   └── process_email_queue.py   # Queue processor
├── run_aimailer.sh              # AI Tooling generation script
├── run_models.sh                # AI Models generation script
├── run_processor.sh             # Queue processing script
├── manage_cache.py              # Cache management utility
├── rotate_logs.sh               # Log rotation script
├── sent_articles.json           # AI Tooling tracking cache
├── sent_articles_models.json    # AI Models tracking cache
├── requirements.txt             # Python dependencies
├── .env.example                # Environment template
├── project.json                # Project metadata
└── README.md                   # This file
```

## 🔧 Monitoring & Maintenance

### Logs
- `aimailer.log` - AI Tooling pipeline logs
- `models.log` - AI Models pipeline logs
- `processor.log` - Email delivery logs
- `rotation.log` - Log rotation logs

### Cache Management
```bash
# View sent articles cache (both types)
python manage_cache.py show

# Clear cache (reset duplicate tracking)
python manage_cache.py clear

# Check cache files directly
cat sent_articles.json sent_articles_models.json
```

### Performance Metrics
- **Emails Per Day**: 2 (AI Tooling + AI Models)
- **Articles Processed**: 200+ per day from 8 sources
- **Articles Selected**: 22 per day (12 + 10)
- **Processing Time**: ~5 minutes per email generation
- **Delivery Reliability**: 99%+ (SQS + retry logic)
- **Duplicate Prevention**: 30-day tracking per email type

## 🛠️ Development

### Testing
```bash
# Test AI Tooling email
python src/run.py --config config --dry-run --max-items 5

# Test AI Models email
python src/run.py --config config_models --dry-run --max-items 5
```

## 📋 Dependencies

- `requests` - HTTP client for fetching content
- `feedparser` - RSS feed parsing
- `boto3` - AWS SQS integration
- `python-dateutil` - Date parsing and handling
- `beautifulsoup4` - HTML processing utilities
- `pyyaml` - Configuration file parsing
- `pytest` - Testing framework

## 🔒 Security

- All credentials stored in environment variables
- HTML content sanitized during extraction
- Rate-limited external requests
- Respects robots.txt and terms of service

## 📄 License

Proprietary - Internal use only

## 👤 Contact

**Owner**: stephen.z.phillips@sparktsl.com

---

**Status**: ✅ Production Ready | **Next Emails**: Daily at 12:00 PM & 3:00 PM | **Cache**: 30-day duplicate prevention per email type

## 🌐 Web Admin for Newsletter Management

AIMailer includes a Django-based web admin interface for managing newsletters, users, and content. This is the recommended way to manage recipients, view sent articles, and configure newsletter settings.

### Accessing the Web Admin

- **Production URL:** https://aimailer.happymonkey.ai/admin
- **Local Development:** http://localhost:8001/admin

### First-Time Setup

1. **Start all services:**
   ```bash
   docker compose up -d --build
   ```
2. **Create a superuser:**
   ```bash
   docker compose exec web python manage.py createsuperuser
   ```
3. **Login:**
   - Visit the admin URL above and log in with your superuser credentials.

### Required Environment Variables

Ensure these are set in your `docker-compose.yml` or `.env`:
- `ALLOWED_HOSTS=aimailer.happymonkey.ai,localhost,127.0.0.1`
- `CSRF_TRUSTED_ORIGINS=https://aimailer.happymonkey.ai`

### Static Files

Static files are automatically collected to `web/staticfiles/` and served by nginx. If you see missing CSS/JS, ensure nginx is configured to serve `/static/` from this directory.

### Troubleshooting
- **403 CSRF Errors:** Make sure `CSRF_TRUSTED_ORIGINS` includes your domain (with `https://`).
- **400 Bad Request:** Add your domain to `ALLOWED_HOSTS`.
- **Static Files 404:** Confirm nginx serves `/static/` from `web/staticfiles/`.

### Features in the Admin
- Manage newsletter recipients and user accounts
- View and edit sent articles
- Configure newsletter settings
- Monitor logs and system status

---
