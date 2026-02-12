#!/bin/bash
cd /var/www/html/AIMailer
source venv/bin/activate
# load .env and export variables
if [ -f .env ]; then
  set -o allexport
  . .env
  set +o allexport
fi

python3 src/run.py --config config_models --max-items 10 >> /var/www/html/AIMailer/models.log 2>&1
