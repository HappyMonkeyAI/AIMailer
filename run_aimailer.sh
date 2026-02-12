#!/bin/bash
# Set base directory to script location
BASE_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"
cd "$BASE_DIR"

echo "$(date): Starting AIMailer execution" >> aimailer.log
source venv/bin/activate
# Use SQS for email sending (disable dry-run)
# load .env and export variables
if [ -f .env ]; then
  set -o allexport
  . .env
  set +o allexport
fi

python3 src/run.py --max-items 12 >> aimailer.log 2>&1
echo "$(date): Finished AIMailer execution" >> aimailer.log
