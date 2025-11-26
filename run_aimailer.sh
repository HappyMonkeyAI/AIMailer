#!/bin/bash
cd /home/stephen/AIMailer
source venv/bin/activate
# Use SQS for email sending (disable dry-run)
python3 src/run.py --max-items 12 >> /home/stephen/AIMailer/aimailer.log 2>&1
