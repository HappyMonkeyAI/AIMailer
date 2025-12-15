#!/bin/bash
echo "$(date): Starting AIMailer execution" >> /var/www/html/happymonkey.ai/AIMailer/aimailer.log
cd /var/www/html/happymonkey.ai/AIMailer
source venv/bin/activate
# Use SQS for email sending (disable dry-run)
# load .env and export variables
if [ -f .env ]; then
  set -o allexport
  . .env
  set +o allexport
fi

python3 src/run.py --max-items 12 >> /var/www/html/happymonkey.ai/AIMailer/aimailer.log 2>&1
echo "$(date): Finished AIMailer execution" >> /var/www/html/happymonkey.ai/AIMailer/aimailer.log
