# SMTP Email Setup for AIMailer

## Gmail SMTP Setup (Recommended)

1. **Enable 2-Factor Authentication** on your Gmail account
2. **Generate App Password**:
   - Go to Google Account settings
   - Security → 2-Step Verification → App passwords
   - Generate password for "Mail"
3. **Update .env file**:
   ```bash
   SMTP_PASS="your-16-character-app-password"
   ```

## Test SMTP Setup
```bash
cd /var/www/html/happymonkey.ai/AIMailer
source venv/bin/activate

# Test with your app password
SMTP_PASS="your-app-password" python3 -c "
import sys
sys.path.insert(0, 'src')
from aimailer.sender import send_email
result = send_email('SMTP Test', '<h1>SMTP Working!</h1>', 'stephen.z.phillips@sparktsl.com', dry_run=False)
print('Result:', result)
"
```

## Alternative SMTP Providers
- **Outlook**: smtp-mail.outlook.com:587
- **Yahoo**: smtp.mail.yahoo.com:587
- **SendGrid**: smtp.sendgrid.net:587

Once SMTP_PASS is set, the processor will automatically send real emails!
