import os
import smtplib
from email.mime.text import MIMEText
from typing import List, Union

# SMTP configuration only
SMTP_HOST = os.environ.get('SMTP_HOST')
SMTP_PORT = int(os.environ.get('SMTP_PORT', 587)) if os.environ.get('SMTP_PORT') else 587
SMTP_USER = os.environ.get('SMTP_USER')
SMTP_PASS = os.environ.get('SMTP_PASS')


def send_email(subject: str, html_body: str, recipients: Union[str, List[str]], dry_run: bool = True) -> bool:
    """Send HTML email to multiple recipients via SMTP. No SQS/SES support.

    If `dry_run` is True, the function only logs the intended action.
    """
    print('send_email called; dry_run=', dry_run)

    # Ensure recipients is a list
    if isinstance(recipients, str):
        recipients = [recipients]

    if dry_run:
        print(f'DRY RUN: would send email to {len(recipients)} recipients: {", ".join(recipients)}')
        return True

    # Require SMTP host and credentials
    if not SMTP_HOST:
        raise RuntimeError('SMTP_HOST not configured')

    try:
        server = smtplib.SMTP(SMTP_HOST, SMTP_PORT)
        server.starttls()
        if SMTP_USER and SMTP_PASS:
            server.login(SMTP_USER, SMTP_PASS)

        success_count = 0
        for recipient in recipients:
            msg = MIMEText(html_body, 'html')
            msg['Subject'] = subject
            msg['From'] = SMTP_USER or 'no-reply@example.com'
            msg['To'] = recipient
            server.sendmail(msg['From'], [recipient], msg.as_string())
            print(f'SMTP email sent to {recipient}')
            success_count += 1

        server.quit()
        return success_count == len(recipients)
    except Exception as e:
        print(f'SMTP failed: {e}')
        return False
