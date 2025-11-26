# Adding Multiple Recipients to AIMailer

## How to Add Recipients

Edit `src/aimailer/config.py` and update the `RECIPIENTS` list:

```python
RECIPIENTS = [
    'stephen.z.phillips@sparktsl.com',
    'colleague@company.com',
    'team-lead@company.com',
    'ai-team@company.com',
]
```

## How It Works

- **SQS Mode**: Creates separate queue messages for each recipient
- **SMTP Mode**: Sends individual emails to each recipient
- **Logging**: Shows total recipient count in logs
- **Error Handling**: Continues sending to other recipients if one fails

## Testing Multiple Recipients

```bash
# Test with dry-run to see recipient list
python src/run.py --dry-run --max-items 3

# Send test email to multiple recipients
python -c "
import sys
sys.path.insert(0, 'src')
from aimailer.sender import send_email
recipients = ['email1@example.com', 'email2@example.com']
send_email('Test', '<h1>Test</h1>', recipients, dry_run=False)
"
```

## Current Configuration

Currently configured to send to:
- stephen.z.phillips@sparktsl.com

To add more recipients, simply edit the `RECIPIENTS` list in `config.py` and the system will automatically send to all addresses on the next scheduled run.

## Notes

- Each recipient gets an individual email (not CC/BCC)
- SQS queues separate messages for reliable delivery
- Failed deliveries to one recipient don't affect others
- All recipients receive identical content
