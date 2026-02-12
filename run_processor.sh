#!/bin/bash
# Set base directory to script location
BASE_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"
cd "$BASE_DIR"

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