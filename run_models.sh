#!/bin/bash
cd /home/stephen/AIMailer
source venv/bin/activate
python3 src/run.py --config config_models --max-items 10 >> /home/stephen/AIMailer/models.log 2>&1
