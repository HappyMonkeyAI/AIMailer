# AIMailer SQS Email Processor

## Overview

The AIMailer uses AWS SQS for reliable email delivery. Emails are queued by the main pipeline and processed separately by the email processor.

## Architecture

1. **AIMailer Pipeline** → Generates emails → **SQS Queue**
2. **Email Processor** → Polls SQS → **Delivers emails** → Removes from queue

## Components

### Queue
- **URL**: `https://sqs.us-east-1.amazonaws.com/900211028177/aimailer-email-queue`
- **Region**: us-east-1
- **Polling**: Every 15 minutes via cron

### Processor Scripts
- `src/process_email_queue.py` - Full processor with SMTP/SES delivery
- `process_queue_dry.py` - Dry-run processor (logs only, no email sending)
- `run_processor.sh` - Smart runner (chooses mode based on SMTP config)

### Cron Jobs
```bash
# Generate weekly emails (Fridays 9 AM)
0 9 * * 5 /var/www/html/happymonkey.ai/AIMailer/run_aimailer.sh

# Process email queue (every 15 minutes)
*/15 * * * * /var/www/html/happymonkey.ai/AIMailer/run_processor.sh >> /var/www/html/happymonkey.ai/AIMailer/processor.log 2>&1
```

## Configuration

### For Dry-Run Mode (Current)
No additional configuration needed. Processor will log email details without sending.

### For SMTP Delivery
Set in `.env`:
```bash
SMTP_HOST="smtp.gmail.com"
SMTP_PORT=587
SMTP_USER="your-email@gmail.com"
SMTP_PASS="your-app-password"
```

### For AWS SES Delivery
Requires AWS SES permissions:
- `ses:SendEmail`
- `ses:ListIdentities`

## Usage

### Manual Processing
```bash
# Process queue once (dry-run)
./run_processor.sh

# Process with full email sending (if SMTP configured)
SMTP_PASS="password" ./run_processor.sh
```

### Monitor Queue
```bash
# Check queue status
aws sqs get-queue-attributes --queue-url https://sqs.us-east-1.amazonaws.com/900211028177/aimailer-email-queue --attribute-names ApproximateNumberOfMessages

# View processor logs
tail -f processor.log
```

## Status

✅ **SQS Queue**: Created and functional  
✅ **Processor**: Implemented with error handling  
✅ **Scheduling**: Automated via cron  
🔄 **Email Delivery**: Dry-run mode (SMTP credentials needed for live sending)

## Next Steps

1. Configure SMTP credentials for live email delivery
2. Set up AWS SES permissions for better delivery
3. Add monitoring/alerting for failed deliveries
