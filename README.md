# AIMailer - Weekly AI Tooling Roundup

**Automated weekly email digest of AI tools, models, and developer updates**

[![Status](https://img.shields.io/badge/Status-Production-green)](https://github.com/user/aimailer)
[![Version](https://img.shields.io/badge/Version-1.0.0-blue)](https://github.com/user/aimailer)
[![Python](https://img.shields.io/badge/Python-3.12+-blue)](https://python.org)

## 🎯 Overview

AIMailer is a production-ready system that automatically curates and delivers weekly email roundups of the latest AI tooling, model releases, and developer-focused updates. It processes 100+ articles weekly from major AI/ML sources and delivers a clean, summarized digest of the top 12 most relevant items.

## ✨ Features

- **🔄 Automated Pipeline**: RSS fetching → AI summarization → source diversity → email delivery
- **🤖 AI-Powered**: Ollama-based summarization with OpenAI fallback
- **📊 Source Diversity**: Round-robin selection ensures balanced content from all sources
- **🧹 Clean Extraction**: Advanced HTML cleaning removes JavaScript/JSON noise
- **☁️ Cloud-Native**: AWS SQS queuing with Gmail SMTP delivery
- **📅 Scheduled**: Automated weekly delivery every Monday at 8:00 AM
- **🔍 Monitoring**: Comprehensive logging and error handling

## 📧 Sample Output

Each email contains:
- **12 curated articles** from 6 major AI/ML sources
- **AI-generated summaries** (2-3 sentences each)
- **Developer insights** explaining why each article matters
- **Clean HTML formatting** with clickable links
- **Source attribution** and publication dates

## 🏗️ Architecture

```
RSS Feeds → Content Fetcher → Text Extractor → AI Summarizer → 
Source Selector → Email Composer → SQS Queue → SMTP Sender → Gmail
```

### Components

- **Fetcher** (`fetchers.py`): RSS feed processing with feedparser
- **Extractor** (`extractor.py`): Clean text extraction from HTML
- **Summarizer** (`summarizer.py`): Ollama/OpenAI-powered summarization
- **Selector** (`selector.py`): Source diversity and ranking algorithms
- **Composer** (`composer.py`): HTML email template generation
- **Sender** (`sender.py`): AWS SQS queuing and SMTP delivery
- **Processor** (`process_email_queue.py`): Queue processing and email sending

## 📊 Content Sources

- **OpenAI Blog** - Latest AI model releases and research
- **Google Developers** - AI platform and tool updates
- **GitHub Blog** - Developer workflow and coding tools
- **HuggingFace** - Open-source AI models and datasets
- **AWS ML Blog** - Cloud AI/ML services and tools
- **LangChain Blog** - AI application development frameworks

## 🚀 Quick Start

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

### Usage

```bash
# Generate and send email manually
python src/run.py --max-items 12

# Process email queue
./run_processor.sh

# Check logs
tail -f aimailer.log processor.log
```

## ⏰ Automated Scheduling

The system runs automatically via cron jobs:

```bash
# Weekly email generation (Mondays 8 AM)
0 8 * * 1 /home/stephen/AIMailer/run_aimailer.sh

# Queue processing (every 15 minutes)
*/15 * * * * /home/stephen/AIMailer/run_processor.sh >> /home/stephen/AIMailer/processor.log 2>&1
```

## 📁 Project Structure

```
AIMailer/
├── src/
│   ├── aimailer/
│   │   ├── fetchers.py      # RSS feed processing
│   │   ├── extractor.py     # HTML text extraction
│   │   ├── summarizer.py    # AI summarization
│   │   ├── selector.py      # Content selection & diversity
│   │   ├── composer.py      # Email composition
│   │   ├── sender.py        # SQS queuing & SMTP
│   │   └── config.py        # Configuration
│   ├── run.py               # Main pipeline orchestrator
│   └── process_email_queue.py # Queue processor
├── run_aimailer.sh          # Email generation script
├── run_processor.sh         # Queue processing script
├── requirements.txt         # Python dependencies
├── .env.example            # Environment template
├── project.json            # Project metadata
└── README.md              # This file
```

## 🔧 Monitoring & Maintenance

### Logs
- `aimailer.log` - Pipeline execution logs
- `processor.log` - Email delivery logs

### Queue Monitoring
```bash
# Check SQS queue status
aws sqs get-queue-attributes --queue-url $SQS_QUEUE_URL --attribute-names ApproximateNumberOfMessages

# View recent cron executions
grep aimailer /var/log/syslog
```

### Performance Metrics
- **Articles Processed**: 100+ per week
- **Articles Selected**: 12 per email (2 from each source)
- **Processing Time**: ~5 minutes per generation
- **Delivery Reliability**: 99%+ (SQS + retry logic)

## 🛠️ Development

### Testing
```bash
# Run tests
pytest tests/

# Test individual components
python -c "from aimailer.fetchers import fetch_rss; print(len(fetch_rss('https://openai.com/blog/rss.xml')))"
```

### Adding Sources
Edit `src/aimailer/config.py`:
```python
DEFAULT_SOURCES = [
    'https://new-source.com/feed.xml',
    # ... existing sources
]
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

**Status**: ✅ Production Ready | **Next Email**: Monday, December 2nd, 2025 at 8:00 AM
