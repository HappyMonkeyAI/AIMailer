import os
import smtplib
from email.mime.text import MIMEText

SMTP_HOST = os.environ.get('SMTP_HOST')
SMTP_PORT = int(os.environ.get('SMTP_PORT', 587)) if os.environ.get('SMTP_PORT') else None
SMTP_USER = os.environ.get('SMTP_USER')
SMTP_PASS = os.environ.get('SMTP_PASS')


def send_email(subject: str, html_body: str, recipient: str, dry_run: bool = True) -> bool:
    """Send HTML email. If dry_run is True, only print action and do not send."""
    print('send_email called; dry_run=', dry_run)
    if dry_run:
        print('DRY RUN: would send email to', recipient)
        return True
    if not SMTP_HOST:
        raise RuntimeError('SMTP_HOST not configured')
    msg = MIMEText(html_body, 'html')
    msg['Subject'] = subject
    msg['From'] = SMTP_USER or 'no-reply@example.com'
    msg['To'] = recipient
    server = smtplib.SMTP(SMTP_HOST, SMTP_PORT or 587)
    server.starttls()
    if SMTP_USER and SMTP_PASS:
        server.login(SMTP_USER, SMTP_PASS)
    server.sendmail(msg['From'], [recipient], msg.as_string())
    server.quit()
    return True
