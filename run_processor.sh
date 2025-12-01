#!/bin/bash
cd /var/www/html/happymonkey.ai/AIMailer
source venv/bin/activate

# Load environment variables from .env file
export $(grep -v '^#' .env | xargs)

# Check if SMTP is configured
if [ -z "$SMTP_PASS" ]; then
    echo "SMTP_PASS not set - running in dry-run mode"
    python3 process_queue_dry.py
else
    echo "SMTP configured - running full processor"
    python3 src/process_email_queue.py
fi
/bin/sh: 1: /var/www/html/happymonkey.ai/AIMailer/run_processor.sh: Permission denied
/bin/sh: 1: /var/www/html/happymonkey.ai/AIMailer/run_processor.sh: Permission denied
/bin/sh: 1: /var/www/html/happymonkey.ai/AIMailer/run_processor.sh: Permission denied
/bin/sh: 1: /var/www/html/happymonkey.ai/AIMailer/run_processor.sh: Permission denied
/bin/sh: 1: /var/www/html/happymonkey.ai/AIMailer/run_processor.sh: Permission denied
/bin/sh: 1: /var/www/html/happymonkey.ai/AIMailer/run_processor.sh: Permission denied
/bin/sh: 1: /var/www/html/happymonkey.ai/AIMailer/run_processor.sh: Permission denied
/bin/sh: 1: /var/www/html/happymonkey.ai/AIMailer/run_processor.sh: Permission denied
/bin/sh: 1: /var/www/html/happymonkey.ai/AIMailer/run_processor.sh: Permission denied
/bin/sh: 1: /var/www/html/happymonkey.ai/AIMailer/run_processor.sh: Permission denied
/bin/sh: 1: /var/www/html/happymonkey.ai/AIMailer/run_processor.sh: Permission denied
/bin/sh: 1: /var/www/html/happymonkey.ai/AIMailer/run_processor.sh: Permission denied
/bin/sh: 1: /var/www/html/happymonkey.ai/AIMailer/run_processor.sh: Permission denied
/bin/sh: 1: /var/www/html/happymonkey.ai/AIMailer/run_processor.sh: Permission denied
/bin/sh: 1: /var/www/html/happymonkey.ai/AIMailer/run_processor.sh: Permission denied
/bin/sh: 1: /var/www/html/happymonkey.ai/AIMailer/run_processor.sh: Permission denied
/bin/sh: 1: /var/www/html/happymonkey.ai/AIMailer/run_processor.sh: Permission denied
/bin/sh: 1: /var/www/html/happymonkey.ai/AIMailer/run_processor.sh: Permission denied
/bin/sh: 1: /var/www/html/happymonkey.ai/AIMailer/run_processor.sh: Permission denied
/bin/sh: 1: /var/www/html/happymonkey.ai/AIMailer/run_processor.sh: Permission denied
/bin/sh: 1: /var/www/html/happymonkey.ai/AIMailer/run_processor.sh: Permission denied
/bin/sh: 1: /var/www/html/happymonkey.ai/AIMailer/run_processor.sh: Permission denied
/bin/sh: 1: /var/www/html/happymonkey.ai/AIMailer/run_processor.sh: Permission denied
/bin/sh: 1: /var/www/html/happymonkey.ai/AIMailer/run_processor.sh: Permission denied
/bin/sh: 1: /var/www/html/happymonkey.ai/AIMailer/run_processor.sh: Permission denied
/bin/sh: 1: /var/www/html/happymonkey.ai/AIMailer/run_processor.sh: Permission denied
/bin/sh: 1: /var/www/html/happymonkey.ai/AIMailer/run_processor.sh: Permission denied
/bin/sh: 1: /var/www/html/happymonkey.ai/AIMailer/run_processor.sh: Text file busy
/bin/sh: 1: /var/www/html/happymonkey.ai/AIMailer/run_processor.sh: Text file busy
/bin/sh: 1: /var/www/html/happymonkey.ai/AIMailer/run_processor.sh: Text file busy
/bin/sh: 1: /var/www/html/happymonkey.ai/AIMailer/run_processor.sh: Text file busy
/bin/sh: 1: /var/www/html/happymonkey.ai/AIMailer/run_processor.sh: Text file busy
/bin/sh: 1: /var/www/html/happymonkey.ai/AIMailer/run_processor.sh: Text file busy
/bin/sh: 1: /var/www/html/happymonkey.ai/AIMailer/run_processor.sh: Text file busy
/bin/sh: 1: /var/www/html/happymonkey.ai/AIMailer/run_processor.sh: Text file busy
/bin/sh: 1: /var/www/html/happymonkey.ai/AIMailer/run_processor.sh: Text file busy
/bin/sh: 1: /var/www/html/happymonkey.ai/AIMailer/run_processor.sh: Text file busy
/bin/sh: 1: /var/www/html/happymonkey.ai/AIMailer/run_processor.sh: Text file busy
/bin/sh: 1: /var/www/html/happymonkey.ai/AIMailer/run_processor.sh: Text file busy
/bin/sh: 1: /var/www/html/happymonkey.ai/AIMailer/run_processor.sh: Text file busy
/bin/sh: 1: /var/www/html/happymonkey.ai/AIMailer/run_processor.sh: Text file busy
/bin/sh: 1: /var/www/html/happymonkey.ai/AIMailer/run_processor.sh: Text file busy
/bin/sh: 1: /var/www/html/happymonkey.ai/AIMailer/run_processor.sh: Text file busy
/bin/sh: 1: /var/www/html/happymonkey.ai/AIMailer/run_processor.sh: Text file busy
/bin/sh: 1: /var/www/html/happymonkey.ai/AIMailer/run_processor.sh: Text file busy
/bin/sh: 1: /var/www/html/happymonkey.ai/AIMailer/run_processor.sh: Text file busy
/bin/sh: 1: /var/www/html/happymonkey.ai/AIMailer/run_processor.sh: Text file busy
/bin/sh: 1: /var/www/html/happymonkey.ai/AIMailer/run_processor.sh: Text file busy
/bin/sh: 1: /var/www/html/happymonkey.ai/AIMailer/run_processor.sh: Text file busy
/bin/sh: 1: /var/www/html/happymonkey.ai/AIMailer/run_processor.sh: Text file busy
/bin/sh: 1: /var/www/html/happymonkey.ai/AIMailer/run_processor.sh: Text file busy
/bin/sh: 1: /var/www/html/happymonkey.ai/AIMailer/run_processor.sh: Text file busy
/bin/sh: 1: /var/www/html/happymonkey.ai/AIMailer/run_processor.sh: Text file busy
/bin/sh: 1: /var/www/html/happymonkey.ai/AIMailer/run_processor.sh: Text file busy
/bin/sh: 1: /var/www/html/happymonkey.ai/AIMailer/run_processor.sh: Text file busy
/bin/sh: 1: /var/www/html/happymonkey.ai/AIMailer/run_processor.sh: Text file busy
/bin/sh: 1: /var/www/html/happymonkey.ai/AIMailer/run_processor.sh: Text file busy
/bin/sh: 1: /var/www/html/happymonkey.ai/AIMailer/run_processor.sh: Text file busy
/bin/sh: 1: /var/www/html/happymonkey.ai/AIMailer/run_processor.sh: Text file busy
/bin/sh: 1: /var/www/html/happymonkey.ai/AIMailer/run_processor.sh: Text file busy
/bin/sh: 1: /var/www/html/happymonkey.ai/AIMailer/run_processor.sh: Text file busy
/bin/sh: 1: /var/www/html/happymonkey.ai/AIMailer/run_processor.sh: Text file busy
/bin/sh: 1: /var/www/html/happymonkey.ai/AIMailer/run_processor.sh: Text file busy
/bin/sh: 1: /var/www/html/happymonkey.ai/AIMailer/run_processor.sh: Text file busy
/bin/sh: 1: /var/www/html/happymonkey.ai/AIMailer/run_processor.sh: Text file busy
/bin/sh: 1: /var/www/html/happymonkey.ai/AIMailer/run_processor.sh: Text file busy
/bin/sh: 1: /var/www/html/happymonkey.ai/AIMailer/run_processor.sh: Text file busy
/bin/sh: 1: /var/www/html/happymonkey.ai/AIMailer/run_processor.sh: Text file busy
/bin/sh: 1: /var/www/html/happymonkey.ai/AIMailer/run_processor.sh: Text file busy
/bin/sh: 1: /var/www/html/happymonkey.ai/AIMailer/run_processor.sh: Text file busy
/bin/sh: 1: /var/www/html/happymonkey.ai/AIMailer/run_processor.sh: Text file busy
/bin/sh: 1: /var/www/html/happymonkey.ai/AIMailer/run_processor.sh: Text file busy
/bin/sh: 1: /var/www/html/happymonkey.ai/AIMailer/run_processor.sh: Text file busy
/bin/sh: 1: /var/www/html/happymonkey.ai/AIMailer/run_processor.sh: Text file busy
/bin/sh: 1: /var/www/html/happymonkey.ai/AIMailer/run_processor.sh: Text file busy
/bin/sh: 1: /var/www/html/happymonkey.ai/AIMailer/run_processor.sh: Text file busy
/bin/sh: 1: /var/www/html/happymonkey.ai/AIMailer/run_processor.sh: Text file busy
/bin/sh: 1: /var/www/html/happymonkey.ai/AIMailer/run_processor.sh: Text file busy
/bin/sh: 1: /var/www/html/happymonkey.ai/AIMailer/run_processor.sh: Text file busy
/bin/sh: 1: /var/www/html/happymonkey.ai/AIMailer/run_processor.sh: Text file busy
/bin/sh: 1: /var/www/html/happymonkey.ai/AIMailer/run_processor.sh: Text file busy
/bin/sh: 1: /var/www/html/happymonkey.ai/AIMailer/run_processor.sh: Text file busy
/bin/sh: 1: /var/www/html/happymonkey.ai/AIMailer/run_processor.sh: Text file busy
/bin/sh: 1: /var/www/html/happymonkey.ai/AIMailer/run_processor.sh: Text file busy
/bin/sh: 1: /var/www/html/happymonkey.ai/AIMailer/run_processor.sh: Text file busy
/bin/sh: 1: /var/www/html/happymonkey.ai/AIMailer/run_processor.sh: Text file busy
/bin/sh: 1: /var/www/html/happymonkey.ai/AIMailer/run_processor.sh: Text file busy
/bin/sh: 1: /var/www/html/happymonkey.ai/AIMailer/run_processor.sh: Text file busy
/bin/sh: 1: /var/www/html/happymonkey.ai/AIMailer/run_processor.sh: Text file busy
/bin/sh: 1: /var/www/html/happymonkey.ai/AIMailer/run_processor.sh: Text file busy
/bin/sh: 1: /var/www/html/happymonkey.ai/AIMailer/run_processor.sh: Text file busy
/bin/sh: 1: /var/www/html/happymonkey.ai/AIMailer/run_processor.sh: Text file busy
/bin/sh: 1: /var/www/html/happymonkey.ai/AIMailer/run_processor.sh: Text file busy
/bin/sh: 1: /var/www/html/happymonkey.ai/AIMailer/run_processor.sh: Text file busy
/bin/sh: 1: /var/www/html/happymonkey.ai/AIMailer/run_processor.sh: Text file busy
/bin/sh: 1: /var/www/html/happymonkey.ai/AIMailer/run_processor.sh: Text file busy
/bin/sh: 1: /var/www/html/happymonkey.ai/AIMailer/run_processor.sh: Text file busy
/bin/sh: 1: /var/www/html/happymonkey.ai/AIMailer/run_processor.sh: Text file busy
/bin/sh: 1: /var/www/html/happymonkey.ai/AIMailer/run_processor.sh: Text file busy
/bin/sh: 1: /var/www/html/happymonkey.ai/AIMailer/run_processor.sh: Text file busy
/bin/sh: 1: /var/www/html/happymonkey.ai/AIMailer/run_processor.sh: Text file busy
/bin/sh: 1: /var/www/html/happymonkey.ai/AIMailer/run_processor.sh: Text file busy
/bin/sh: 1: /var/www/html/happymonkey.ai/AIMailer/run_processor.sh: Text file busy
/bin/sh: 1: /var/www/html/happymonkey.ai/AIMailer/run_processor.sh: Text file busy
/bin/sh: 1: /var/www/html/happymonkey.ai/AIMailer/run_processor.sh: Text file busy
/bin/sh: 1: /var/www/html/happymonkey.ai/AIMailer/run_processor.sh: Text file busy
/bin/sh: 1: /var/www/html/happymonkey.ai/AIMailer/run_processor.sh: Text file busy
/bin/sh: 1: /var/www/html/happymonkey.ai/AIMailer/run_processor.sh: Text file busy
/bin/sh: 1: /var/www/html/happymonkey.ai/AIMailer/run_processor.sh: Text file busy
/bin/sh: 1: /var/www/html/happymonkey.ai/AIMailer/run_processor.sh: Text file busy
/bin/sh: 1: /var/www/html/happymonkey.ai/AIMailer/run_processor.sh: Text file busy
/bin/sh: 1: /var/www/html/happymonkey.ai/AIMailer/run_processor.sh: Text file busy
/bin/sh: 1: /var/www/html/happymonkey.ai/AIMailer/run_processor.sh: Text file busy
/bin/sh: 1: /var/www/html/happymonkey.ai/AIMailer/run_processor.sh: Text file busy
/bin/sh: 1: /var/www/html/happymonkey.ai/AIMailer/run_processor.sh: Text file busy
/bin/sh: 1: /var/www/html/happymonkey.ai/AIMailer/run_processor.sh: Text file busy
/bin/sh: 1: /var/www/html/happymonkey.ai/AIMailer/run_processor.sh: Text file busy
/bin/sh: 1: /var/www/html/happymonkey.ai/AIMailer/run_processor.sh: Text file busy
/bin/sh: 1: /var/www/html/happymonkey.ai/AIMailer/run_processor.sh: Text file busy
/bin/sh: 1: /var/www/html/happymonkey.ai/AIMailer/run_processor.sh: Text file busy
/bin/sh: 1: /var/www/html/happymonkey.ai/AIMailer/run_processor.sh: Text file busy
/bin/sh: 1: /var/www/html/happymonkey.ai/AIMailer/run_processor.sh: Text file busy
/bin/sh: 1: /var/www/html/happymonkey.ai/AIMailer/run_processor.sh: Text file busy
/bin/sh: 1: /var/www/html/happymonkey.ai/AIMailer/run_processor.sh: Text file busy
/bin/sh: 1: /var/www/html/happymonkey.ai/AIMailer/run_processor.sh: Text file busy
/bin/sh: 1: /var/www/html/happymonkey.ai/AIMailer/run_processor.sh: Text file busy
/bin/sh: 1: /var/www/html/happymonkey.ai/AIMailer/run_processor.sh: Text file busy
/bin/sh: 1: /var/www/html/happymonkey.ai/AIMailer/run_processor.sh: Text file busy
/bin/sh: 1: /var/www/html/happymonkey.ai/AIMailer/run_processor.sh: Text file busy
/bin/sh: 1: /var/www/html/happymonkey.ai/AIMailer/run_processor.sh: Text file busy
/bin/sh: 1: /var/www/html/happymonkey.ai/AIMailer/run_processor.sh: Text file busy
/bin/sh: 1: /var/www/html/happymonkey.ai/AIMailer/run_processor.sh: Text file busy
/bin/sh: 1: /var/www/html/happymonkey.ai/AIMailer/run_processor.sh: Text file busy
/bin/sh: 1: /var/www/html/happymonkey.ai/AIMailer/run_processor.sh: Text file busy
/bin/sh: 1: /var/www/html/happymonkey.ai/AIMailer/run_processor.sh: Text file busy
/bin/sh: 1: /var/www/html/happymonkey.ai/AIMailer/run_processor.sh: Text file busy
/bin/sh: 1: /var/www/html/happymonkey.ai/AIMailer/run_processor.sh: Text file busy
/bin/sh: 1: /var/www/html/happymonkey.ai/AIMailer/run_processor.sh: Text file busy
/bin/sh: 1: /var/www/html/happymonkey.ai/AIMailer/run_processor.sh: Text file busy
/bin/sh: 1: /var/www/html/happymonkey.ai/AIMailer/run_processor.sh: Text file busy
/bin/sh: 1: /var/www/html/happymonkey.ai/AIMailer/run_processor.sh: Text file busy
/bin/sh: 1: /var/www/html/happymonkey.ai/AIMailer/run_processor.sh: Text file busy
/bin/sh: 1: /var/www/html/happymonkey.ai/AIMailer/run_processor.sh: Text file busy
/bin/sh: 1: /var/www/html/happymonkey.ai/AIMailer/run_processor.sh: Text file busy
/bin/sh: 1: /var/www/html/happymonkey.ai/AIMailer/run_processor.sh: Text file busy
/bin/sh: 1: /var/www/html/happymonkey.ai/AIMailer/run_processor.sh: Text file busy
/bin/sh: 1: /var/www/html/happymonkey.ai/AIMailer/run_processor.sh: Text file busy
/bin/sh: 1: /var/www/html/happymonkey.ai/AIMailer/run_processor.sh: Text file busy
/bin/sh: 1: /var/www/html/happymonkey.ai/AIMailer/run_processor.sh: Text file busy
/bin/sh: 1: /var/www/html/happymonkey.ai/AIMailer/run_processor.sh: Text file busy
/bin/sh: 1: /var/www/html/happymonkey.ai/AIMailer/run_processor.sh: Text file busy
/bin/sh: 1: /var/www/html/happymonkey.ai/AIMailer/run_processor.sh: Text file busy
/bin/sh: 1: /var/www/html/happymonkey.ai/AIMailer/run_processor.sh: Text file busy
/bin/sh: 1: /var/www/html/happymonkey.ai/AIMailer/run_processor.sh: Text file busy
/bin/sh: 1: /var/www/html/happymonkey.ai/AIMailer/run_processor.sh: Text file busy
/bin/sh: 1: /var/www/html/happymonkey.ai/AIMailer/run_processor.sh: Text file busy
/bin/sh: 1: /var/www/html/happymonkey.ai/AIMailer/run_processor.sh: Text file busy
/bin/sh: 1: /var/www/html/happymonkey.ai/AIMailer/run_processor.sh: Text file busy
/bin/sh: 1: /var/www/html/happymonkey.ai/AIMailer/run_processor.sh: Text file busy
/bin/sh: 1: /var/www/html/happymonkey.ai/AIMailer/run_processor.sh: Text file busy
/bin/sh: 1: /var/www/html/happymonkey.ai/AIMailer/run_processor.sh: Text file busy
/bin/sh: 1: /var/www/html/happymonkey.ai/AIMailer/run_processor.sh: Text file busy
/bin/sh: 1: /var/www/html/happymonkey.ai/AIMailer/run_processor.sh: Text file busy
/bin/sh: 1: /var/www/html/happymonkey.ai/AIMailer/run_processor.sh: Text file busy
/bin/sh: 1: /var/www/html/happymonkey.ai/AIMailer/run_processor.sh: Text file busy
/bin/sh: 1: /var/www/html/happymonkey.ai/AIMailer/run_processor.sh: Text file busy
/bin/sh: 1: /var/www/html/happymonkey.ai/AIMailer/run_processor.sh: Text file busy
/bin/sh: 1: /var/www/html/happymonkey.ai/AIMailer/run_processor.sh: Text file busy
/bin/sh: 1: /var/www/html/happymonkey.ai/AIMailer/run_processor.sh: Text file busy
/bin/sh: 1: /var/www/html/happymonkey.ai/AIMailer/run_processor.sh: Text file busy
/bin/sh: 1: /var/www/html/happymonkey.ai/AIMailer/run_processor.sh: Text file busy
/bin/sh: 1: /var/www/html/happymonkey.ai/AIMailer/run_processor.sh: Text file busy
/bin/sh: 1: /var/www/html/happymonkey.ai/AIMailer/run_processor.sh: Text file busy
/bin/sh: 1: /var/www/html/happymonkey.ai/AIMailer/run_processor.sh: Text file busy
/bin/sh: 1: /var/www/html/happymonkey.ai/AIMailer/run_processor.sh: Text file busy
/bin/sh: 1: /var/www/html/happymonkey.ai/AIMailer/run_processor.sh: Text file busy
/bin/sh: 1: /var/www/html/happymonkey.ai/AIMailer/run_processor.sh: Text file busy
/bin/sh: 1: /var/www/html/happymonkey.ai/AIMailer/run_processor.sh: Text file busy
/bin/sh: 1: /var/www/html/happymonkey.ai/AIMailer/run_processor.sh: Text file busy
/bin/sh: 1: /var/www/html/happymonkey.ai/AIMailer/run_processor.sh: Text file busy
/bin/sh: 1: /var/www/html/happymonkey.ai/AIMailer/run_processor.sh: Text file busy
/bin/sh: 1: /var/www/html/happymonkey.ai/AIMailer/run_processor.sh: Text file busy
/bin/sh: 1: /var/www/html/happymonkey.ai/AIMailer/run_processor.sh: Text file busy
/bin/sh: 1: /var/www/html/happymonkey.ai/AIMailer/run_processor.sh: Text file busy
/bin/sh: 1: /var/www/html/happymonkey.ai/AIMailer/run_processor.sh: Text file busy
/bin/sh: 1: /var/www/html/happymonkey.ai/AIMailer/run_processor.sh: Text file busy
/bin/sh: 1: /var/www/html/happymonkey.ai/AIMailer/run_processor.sh: Text file busy
/bin/sh: 1: /var/www/html/happymonkey.ai/AIMailer/run_processor.sh: Text file busy
/bin/sh: 1: /var/www/html/happymonkey.ai/AIMailer/run_processor.sh: Text file busy
/bin/sh: 1: /var/www/html/happymonkey.ai/AIMailer/run_processor.sh: Text file busy
/bin/sh: 1: /var/www/html/happymonkey.ai/AIMailer/run_processor.sh: Text file busy
/bin/sh: 1: /var/www/html/happymonkey.ai/AIMailer/run_processor.sh: Text file busy
/bin/sh: 1: /var/www/html/happymonkey.ai/AIMailer/run_processor.sh: Text file busy
/bin/sh: 1: /var/www/html/happymonkey.ai/AIMailer/run_processor.sh: Text file busy
/bin/sh: 1: /var/www/html/happymonkey.ai/AIMailer/run_processor.sh: Text file busy
/bin/sh: 1: /var/www/html/happymonkey.ai/AIMailer/run_processor.sh: Text file busy
/bin/sh: 1: /var/www/html/happymonkey.ai/AIMailer/run_processor.sh: Text file busy
/bin/sh: 1: /var/www/html/happymonkey.ai/AIMailer/run_processor.sh: Text file busy
/bin/sh: 1: /var/www/html/happymonkey.ai/AIMailer/run_processor.sh: Text file busy
/bin/sh: 1: /var/www/html/happymonkey.ai/AIMailer/run_processor.sh: Text file busy
/bin/sh: 1: /var/www/html/happymonkey.ai/AIMailer/run_processor.sh: Text file busy
/bin/sh: 1: /var/www/html/happymonkey.ai/AIMailer/run_processor.sh: Text file busy
/bin/sh: 1: /var/www/html/happymonkey.ai/AIMailer/run_processor.sh: Text file busy
/bin/sh: 1: /var/www/html/happymonkey.ai/AIMailer/run_processor.sh: Text file busy
/bin/sh: 1: /var/www/html/happymonkey.ai/AIMailer/run_processor.sh: Text file busy
/bin/sh: 1: /var/www/html/happymonkey.ai/AIMailer/run_processor.sh: Text file busy
/bin/sh: 1: /var/www/html/happymonkey.ai/AIMailer/run_processor.sh: Text file busy
/bin/sh: 1: /var/www/html/happymonkey.ai/AIMailer/run_processor.sh: Text file busy
/bin/sh: 1: /var/www/html/happymonkey.ai/AIMailer/run_processor.sh: Text file busy
/bin/sh: 1: /var/www/html/happymonkey.ai/AIMailer/run_processor.sh: Text file busy
/bin/sh: 1: /var/www/html/happymonkey.ai/AIMailer/run_processor.sh: Text file busy
/bin/sh: 1: /var/www/html/happymonkey.ai/AIMailer/run_processor.sh: Text file busy
/bin/sh: 1: /var/www/html/happymonkey.ai/AIMailer/run_processor.sh: Text file busy
/bin/sh: 1: /var/www/html/happymonkey.ai/AIMailer/run_processor.sh: Text file busy
/bin/sh: 1: /var/www/html/happymonkey.ai/AIMailer/run_processor.sh: Text file busy
/bin/sh: 1: /var/www/html/happymonkey.ai/AIMailer/run_processor.sh: Text file busy
/bin/sh: 1: /var/www/html/happymonkey.ai/AIMailer/run_processor.sh: Text file busy
/bin/sh: 1: /var/www/html/happymonkey.ai/AIMailer/run_processor.sh: Text file busy
/bin/sh: 1: /var/www/html/happymonkey.ai/AIMailer/run_processor.sh: Text file busy
/bin/sh: 1: /var/www/html/happymonkey.ai/AIMailer/run_processor.sh: Text file busy
/bin/sh: 1: /var/www/html/happymonkey.ai/AIMailer/run_processor.sh: Text file busy
/bin/sh: 1: /var/www/html/happymonkey.ai/AIMailer/run_processor.sh: Text file busy
/bin/sh: 1: /var/www/html/happymonkey.ai/AIMailer/run_processor.sh: Text file busy
/bin/sh: 1: /var/www/html/happymonkey.ai/AIMailer/run_processor.sh: Text file busy
/bin/sh: 1: /var/www/html/happymonkey.ai/AIMailer/run_processor.sh: Text file busy
/bin/sh: 1: /var/www/html/happymonkey.ai/AIMailer/run_processor.sh: Text file busy
/bin/sh: 1: /var/www/html/happymonkey.ai/AIMailer/run_processor.sh: Text file busy
/bin/sh: 1: /var/www/html/happymonkey.ai/AIMailer/run_processor.sh: Text file busy
/bin/sh: 1: /var/www/html/happymonkey.ai/AIMailer/run_processor.sh: Text file busy
/bin/sh: 1: /var/www/html/happymonkey.ai/AIMailer/run_processor.sh: Text file busy
/bin/sh: 1: /var/www/html/happymonkey.ai/AIMailer/run_processor.sh: Text file busy
/bin/sh: 1: /var/www/html/happymonkey.ai/AIMailer/run_processor.sh: Text file busy
/bin/sh: 1: /var/www/html/happymonkey.ai/AIMailer/run_processor.sh: Text file busy
/bin/sh: 1: /var/www/html/happymonkey.ai/AIMailer/run_processor.sh: Text file busy
/bin/sh: 1: /var/www/html/happymonkey.ai/AIMailer/run_processor.sh: Text file busy
/bin/sh: 1: /var/www/html/happymonkey.ai/AIMailer/run_processor.sh: Text file busy
/bin/sh: 1: /var/www/html/happymonkey.ai/AIMailer/run_processor.sh: Text file busy
/bin/sh: 1: /var/www/html/happymonkey.ai/AIMailer/run_processor.sh: Text file busy
/bin/sh: 1: /var/www/html/happymonkey.ai/AIMailer/run_processor.sh: Text file busy
/bin/sh: 1: /var/www/html/happymonkey.ai/AIMailer/run_processor.sh: Text file busy
/bin/sh: 1: /var/www/html/happymonkey.ai/AIMailer/run_processor.sh: Text file busy
/bin/sh: 1: /var/www/html/happymonkey.ai/AIMailer/run_processor.sh: Text file busy
/bin/sh: 1: /var/www/html/happymonkey.ai/AIMailer/run_processor.sh: Text file busy
/bin/sh: 1: /var/www/html/happymonkey.ai/AIMailer/run_processor.sh: Text file busy
/bin/sh: 1: /var/www/html/happymonkey.ai/AIMailer/run_processor.sh: Text file busy
/bin/sh: 1: /var/www/html/happymonkey.ai/AIMailer/run_processor.sh: Text file busy
/bin/sh: 1: /var/www/html/happymonkey.ai/AIMailer/run_processor.sh: Text file busy
/bin/sh: 1: /var/www/html/happymonkey.ai/AIMailer/run_processor.sh: Text file busy
/bin/sh: 1: /var/www/html/happymonkey.ai/AIMailer/run_processor.sh: Text file busy
/bin/sh: 1: /var/www/html/happymonkey.ai/AIMailer/run_processor.sh: Text file busy
/bin/sh: 1: /var/www/html/happymonkey.ai/AIMailer/run_processor.sh: Text file busy
/bin/sh: 1: /var/www/html/happymonkey.ai/AIMailer/run_processor.sh: Text file busy
/bin/sh: 1: /var/www/html/happymonkey.ai/AIMailer/run_processor.sh: Text file busy
/bin/sh: 1: /var/www/html/happymonkey.ai/AIMailer/run_processor.sh: Text file busy
/bin/sh: 1: /var/www/html/happymonkey.ai/AIMailer/run_processor.sh: Text file busy
/bin/sh: 1: /var/www/html/happymonkey.ai/AIMailer/run_processor.sh: Text file busy
/bin/sh: 1: /var/www/html/happymonkey.ai/AIMailer/run_processor.sh: Text file busy
/bin/sh: 1: /var/www/html/happymonkey.ai/AIMailer/run_processor.sh: Text file busy
/bin/sh: 1: /var/www/html/happymonkey.ai/AIMailer/run_processor.sh: Text file busy
/bin/sh: 1: /var/www/html/happymonkey.ai/AIMailer/run_processor.sh: Text file busy
/bin/sh: 1: /var/www/html/happymonkey.ai/AIMailer/run_processor.sh: Text file busy
/bin/sh: 1: /var/www/html/happymonkey.ai/AIMailer/run_processor.sh: Text file busy
/bin/sh: 1: /var/www/html/happymonkey.ai/AIMailer/run_processor.sh: Text file busy
/bin/sh: 1: /var/www/html/happymonkey.ai/AIMailer/run_processor.sh: Text file busy
/bin/sh: 1: /var/www/html/happymonkey.ai/AIMailer/run_processor.sh: Text file busy
/bin/sh: 1: /var/www/html/happymonkey.ai/AIMailer/run_processor.sh: Text file busy
/bin/sh: 1: /var/www/html/happymonkey.ai/AIMailer/run_processor.sh: Text file busy
/bin/sh: 1: /var/www/html/happymonkey.ai/AIMailer/run_processor.sh: Text file busy
/bin/sh: 1: /var/www/html/happymonkey.ai/AIMailer/run_processor.sh: Text file busy
/bin/sh: 1: /var/www/html/happymonkey.ai/AIMailer/run_processor.sh: Text file busy
/bin/sh: 1: /var/www/html/happymonkey.ai/AIMailer/run_processor.sh: Text file busy
/bin/sh: 1: /var/www/html/happymonkey.ai/AIMailer/run_processor.sh: Text file busy
/bin/sh: 1: /var/www/html/happymonkey.ai/AIMailer/run_processor.sh: Text file busy
/bin/sh: 1: /var/www/html/happymonkey.ai/AIMailer/run_processor.sh: Text file busy
/bin/sh: 1: /var/www/html/happymonkey.ai/AIMailer/run_processor.sh: Text file busy
/bin/sh: 1: /var/www/html/happymonkey.ai/AIMailer/run_processor.sh: Text file busy
/bin/sh: 1: /var/www/html/happymonkey.ai/AIMailer/run_processor.sh: Text file busy
/bin/sh: 1: /var/www/html/happymonkey.ai/AIMailer/run_processor.sh: Text file busy
/bin/sh: 1: /var/www/html/happymonkey.ai/AIMailer/run_processor.sh: Text file busy
/bin/sh: 1: /var/www/html/happymonkey.ai/AIMailer/run_processor.sh: Text file busy
/bin/sh: 1: /var/www/html/happymonkey.ai/AIMailer/run_processor.sh: Text file busy
/bin/sh: 1: /var/www/html/happymonkey.ai/AIMailer/run_processor.sh: Text file busy
/bin/sh: 1: /var/www/html/happymonkey.ai/AIMailer/run_processor.sh: Text file busy
/bin/sh: 1: /var/www/html/happymonkey.ai/AIMailer/run_processor.sh: Text file busy
/bin/sh: 1: /var/www/html/happymonkey.ai/AIMailer/run_processor.sh: Text file busy
/bin/sh: 1: /var/www/html/happymonkey.ai/AIMailer/run_processor.sh: Text file busy
/bin/sh: 1: /var/www/html/happymonkey.ai/AIMailer/run_processor.sh: Text file busy
/bin/sh: 1: /var/www/html/happymonkey.ai/AIMailer/run_processor.sh: Text file busy
/bin/sh: 1: /var/www/html/happymonkey.ai/AIMailer/run_processor.sh: Text file busy
/bin/sh: 1: /var/www/html/happymonkey.ai/AIMailer/run_processor.sh: Text file busy
/bin/sh: 1: /var/www/html/happymonkey.ai/AIMailer/run_processor.sh: Text file busy
/bin/sh: 1: /var/www/html/happymonkey.ai/AIMailer/run_processor.sh: Text file busy
/bin/sh: 1: /var/www/html/happymonkey.ai/AIMailer/run_processor.sh: Text file busy
/bin/sh: 1: /var/www/html/happymonkey.ai/AIMailer/run_processor.sh: Text file busy
/bin/sh: 1: /var/www/html/happymonkey.ai/AIMailer/run_processor.sh: Text file busy
/bin/sh: 1: /var/www/html/happymonkey.ai/AIMailer/run_processor.sh: Text file busy
/bin/sh: 1: /var/www/html/happymonkey.ai/AIMailer/run_processor.sh: Text file busy
/bin/sh: 1: /var/www/html/happymonkey.ai/AIMailer/run_processor.sh: Text file busy
/bin/sh: 1: /var/www/html/happymonkey.ai/AIMailer/run_processor.sh: Text file busy
/bin/sh: 1: /var/www/html/happymonkey.ai/AIMailer/run_processor.sh: Text file busy
/bin/sh: 1: /var/www/html/happymonkey.ai/AIMailer/run_processor.sh: Text file busy
/bin/sh: 1: /var/www/html/happymonkey.ai/AIMailer/run_processor.sh: Text file busy
/bin/sh: 1: /var/www/html/happymonkey.ai/AIMailer/run_processor.sh: Text file busy
/bin/sh: 1: /var/www/html/happymonkey.ai/AIMailer/run_processor.sh: Text file busy
/bin/sh: 1: /var/www/html/happymonkey.ai/AIMailer/run_processor.sh: Text file busy
/bin/sh: 1: /var/www/html/happymonkey.ai/AIMailer/run_processor.sh: Text file busy
/bin/sh: 1: /var/www/html/happymonkey.ai/AIMailer/run_processor.sh: Text file busy
/bin/sh: 1: /var/www/html/happymonkey.ai/AIMailer/run_processor.sh: Text file busy
/bin/sh: 1: /var/www/html/happymonkey.ai/AIMailer/run_processor.sh: Text file busy
/bin/sh: 1: /var/www/html/happymonkey.ai/AIMailer/run_processor.sh: Text file busy
/bin/sh: 1: /var/www/html/happymonkey.ai/AIMailer/run_processor.sh: Text file busy
/bin/sh: 1: /var/www/html/happymonkey.ai/AIMailer/run_processor.sh: Text file busy
/bin/sh: 1: /var/www/html/happymonkey.ai/AIMailer/run_processor.sh: Text file busy
/bin/sh: 1: /var/www/html/happymonkey.ai/AIMailer/run_processor.sh: Text file busy
/bin/sh: 1: /var/www/html/happymonkey.ai/AIMailer/run_processor.sh: Text file busy
/bin/sh: 1: /var/www/html/happymonkey.ai/AIMailer/run_processor.sh: Text file busy
/bin/sh: 1: /var/www/html/happymonkey.ai/AIMailer/run_processor.sh: Text file busy
/bin/sh: 1: /var/www/html/happymonkey.ai/AIMailer/run_processor.sh: Text file busy
/bin/sh: 1: /var/www/html/happymonkey.ai/AIMailer/run_processor.sh: Text file busy
/bin/sh: 1: /var/www/html/happymonkey.ai/AIMailer/run_processor.sh: Text file busy
/bin/sh: 1: /var/www/html/happymonkey.ai/AIMailer/run_processor.sh: Text file busy
/bin/sh: 1: /var/www/html/happymonkey.ai/AIMailer/run_processor.sh: Text file busy
/bin/sh: 1: /var/www/html/happymonkey.ai/AIMailer/run_processor.sh: Text file busy
/bin/sh: 1: /var/www/html/happymonkey.ai/AIMailer/run_processor.sh: Text file busy
/bin/sh: 1: /var/www/html/happymonkey.ai/AIMailer/run_processor.sh: Text file busy
/bin/sh: 1: /var/www/html/happymonkey.ai/AIMailer/run_processor.sh: Text file busy
/bin/sh: 1: /var/www/html/happymonkey.ai/AIMailer/run_processor.sh: Text file busy
/bin/sh: 1: /var/www/html/happymonkey.ai/AIMailer/run_processor.sh: Text file busy
/bin/sh: 1: /var/www/html/happymonkey.ai/AIMailer/run_processor.sh: Text file busy
/bin/sh: 1: /var/www/html/happymonkey.ai/AIMailer/run_processor.sh: Text file busy
/bin/sh: 1: /var/www/html/happymonkey.ai/AIMailer/run_processor.sh: Text file busy
/bin/sh: 1: /var/www/html/happymonkey.ai/AIMailer/run_processor.sh: Text file busy
/bin/sh: 1: /var/www/html/happymonkey.ai/AIMailer/run_processor.sh: Text file busy
/bin/sh: 1: /var/www/html/happymonkey.ai/AIMailer/run_processor.sh: Text file busy
/bin/sh: 1: /var/www/html/happymonkey.ai/AIMailer/run_processor.sh: Text file busy
/bin/sh: 1: /var/www/html/happymonkey.ai/AIMailer/run_processor.sh: Text file busy
/bin/sh: 1: /var/www/html/happymonkey.ai/AIMailer/run_processor.sh: Text file busy
/bin/sh: 1: /var/www/html/happymonkey.ai/AIMailer/run_processor.sh: Text file busy
/bin/sh: 1: /var/www/html/happymonkey.ai/AIMailer/run_processor.sh: Text file busy
/bin/sh: 1: /var/www/html/happymonkey.ai/AIMailer/run_processor.sh: Text file busy
/bin/sh: 1: /var/www/html/happymonkey.ai/AIMailer/run_processor.sh: Text file busy
/bin/sh: 1: /var/www/html/happymonkey.ai/AIMailer/run_processor.sh: Text file busy
/bin/sh: 1: /var/www/html/happymonkey.ai/AIMailer/run_processor.sh: Text file busy
/bin/sh: 1: /var/www/html/happymonkey.ai/AIMailer/run_processor.sh: Text file busy
/bin/sh: 1: /var/www/html/happymonkey.ai/AIMailer/run_processor.sh: Text file busy
/bin/sh: 1: /var/www/html/happymonkey.ai/AIMailer/run_processor.sh: Text file busy
/bin/sh: 1: /var/www/html/happymonkey.ai/AIMailer/run_processor.sh: Text file busy
/bin/sh: 1: /var/www/html/happymonkey.ai/AIMailer/run_processor.sh: Text file busy
/bin/sh: 1: /var/www/html/happymonkey.ai/AIMailer/run_processor.sh: Text file busy
/bin/sh: 1: /var/www/html/happymonkey.ai/AIMailer/run_processor.sh: Text file busy
/bin/sh: 1: /var/www/html/happymonkey.ai/AIMailer/run_processor.sh: Text file busy
/bin/sh: 1: /var/www/html/happymonkey.ai/AIMailer/run_processor.sh: Text file busy
/bin/sh: 1: /var/www/html/happymonkey.ai/AIMailer/run_processor.sh: Text file busy
/bin/sh: 1: /var/www/html/happymonkey.ai/AIMailer/run_processor.sh: Text file busy
/bin/sh: 1: /var/www/html/happymonkey.ai/AIMailer/run_processor.sh: Text file busy
/bin/sh: 1: /var/www/html/happymonkey.ai/AIMailer/run_processor.sh: Text file busy
/bin/sh: 1: /var/www/html/happymonkey.ai/AIMailer/run_processor.sh: Text file busy
/bin/sh: 1: /var/www/html/happymonkey.ai/AIMailer/run_processor.sh: Text file busy
/bin/sh: 1: /var/www/html/happymonkey.ai/AIMailer/run_processor.sh: Text file busy
/bin/sh: 1: /var/www/html/happymonkey.ai/AIMailer/run_processor.sh: Text file busy
/bin/sh: 1: /var/www/html/happymonkey.ai/AIMailer/run_processor.sh: Text file busy
/bin/sh: 1: /var/www/html/happymonkey.ai/AIMailer/run_processor.sh: Text file busy
/bin/sh: 1: /var/www/html/happymonkey.ai/AIMailer/run_processor.sh: Text file busy
/bin/sh: 1: /var/www/html/happymonkey.ai/AIMailer/run_processor.sh: Text file busy
/bin/sh: 1: /var/www/html/happymonkey.ai/AIMailer/run_processor.sh: Text file busy
/bin/sh: 1: /var/www/html/happymonkey.ai/AIMailer/run_processor.sh: Text file busy
/bin/sh: 1: /var/www/html/happymonkey.ai/AIMailer/run_processor.sh: Text file busy
/bin/sh: 1: /var/www/html/happymonkey.ai/AIMailer/run_processor.sh: Text file busy
/bin/sh: 1: /var/www/html/happymonkey.ai/AIMailer/run_processor.sh: Text file busy
/bin/sh: 1: /var/www/html/happymonkey.ai/AIMailer/run_processor.sh: Text file busy
/bin/sh: 1: /var/www/html/happymonkey.ai/AIMailer/run_processor.sh: Text file busy
/bin/sh: 1: /var/www/html/happymonkey.ai/AIMailer/run_processor.sh: Text file busy
/bin/sh: 1: /var/www/html/happymonkey.ai/AIMailer/run_processor.sh: Text file busy
/bin/sh: 1: /var/www/html/happymonkey.ai/AIMailer/run_processor.sh: Text file busy
/bin/sh: 1: /var/www/html/happymonkey.ai/AIMailer/run_processor.sh: Text file busy
/bin/sh: 1: /var/www/html/happymonkey.ai/AIMailer/run_processor.sh: Text file busy
/bin/sh: 1: /var/www/html/happymonkey.ai/AIMailer/run_processor.sh: Text file busy
/bin/sh: 1: /var/www/html/happymonkey.ai/AIMailer/run_processor.sh: Text file busy
/bin/sh: 1: /var/www/html/happymonkey.ai/AIMailer/run_processor.sh: Text file busy
/bin/sh: 1: /var/www/html/happymonkey.ai/AIMailer/run_processor.sh: Text file busy
/bin/sh: 1: /var/www/html/happymonkey.ai/AIMailer/run_processor.sh: Text file busy
/bin/sh: 1: /var/www/html/happymonkey.ai/AIMailer/run_processor.sh: Text file busy
/bin/sh: 1: /var/www/html/happymonkey.ai/AIMailer/run_processor.sh: Text file busy
/bin/sh: 1: /var/www/html/happymonkey.ai/AIMailer/run_processor.sh: Text file busy
/bin/sh: 1: /var/www/html/happymonkey.ai/AIMailer/run_processor.sh: Text file busy
/bin/sh: 1: /var/www/html/happymonkey.ai/AIMailer/run_processor.sh: Text file busy
/bin/sh: 1: /var/www/html/happymonkey.ai/AIMailer/run_processor.sh: Text file busy
