#!/bin/bash
echo "$(date): Starting AIMailer execution" >> /var/www/html/AIMailer/aimailer.log
cd /var/www/html/AIMailer
source venv/bin/activate
# Use SQS for email sending (disable dry-run)
# load .env and export variables
if [ -f .env ]; then
  set -o allexport
  . .env
  set +o allexport
fi

python3 src/run.py --max-items 12 >> /var/www/html/AIMailer/aimailer.log 2>&1
echo "$(date): Finished AIMailer execution" >> /var/www/html/AIMailer/aimailer.log
