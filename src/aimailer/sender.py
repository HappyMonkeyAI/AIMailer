import os
import smtplib
from email.mime.text import MIMEText
from typing import List, Union, Dict

# SMTP configuration only
SMTP_HOST = os.environ.get('SMTP_HOST')
SMTP_PORT = int(os.environ.get('SMTP_PORT', 587)) if os.environ.get('SMTP_PORT') else 587
SMTP_USER = os.environ.get('SMTP_USER')
SMTP_PASS = os.environ.get('SMTP_PASS')


def send_email(subject: str, html_body: str, recipients: Union[str, List[str], List[Dict]], dry_run: bool = True,
               sender_email: str = None, sender_name: str = None) -> int:
    """Send HTML email to multiple recipients via SMTP.

    Recipients can be a list of strings (emails) or dictionaries ({'email': '...', 'unsubscribe_url': '...'}).
    If a dictionary is provided, '{{ unsubscribe_url }}' in html_body will be replaced.

    Returns the number of successfully sent emails.
    """
    print('send_email called; dry_run=', dry_run)

    # Ensure recipients is a list
    if isinstance(recipients, str):
        recipients = [recipients]

    if dry_run:
        count = len(recipients)
        sample = recipients[0] if count > 0 else "none"
        print(f'DRY RUN: would send email to {count} recipients. Sample: {sample}')
        return count

    # Require SMTP host and credentials
    if not SMTP_HOST:
        raise RuntimeError('SMTP_HOST not configured')

    try:
        if SMTP_PORT == 465:
            server = smtplib.SMTP_SSL(SMTP_HOST, SMTP_PORT)
        else:
            server = smtplib.SMTP(SMTP_HOST, SMTP_PORT)
            server.starttls()
            
        if SMTP_USER and SMTP_PASS:
            server.login(SMTP_USER, SMTP_PASS)

        # Determine From address
        from_addr = sender_email or SMTP_USER or 'no-reply@example.com'
        if sender_name:
            from_addr = f"{sender_name} <{from_addr}>"

        success_count = 0
        envelope_from = SMTP_USER or sender_email or 'no-reply@example.com'

        for recipient in recipients:
            email_addr = recipient
            body = html_body

            if isinstance(recipient, dict):
                email_addr = recipient.get('email')
                unsubscribe_url = recipient.get('unsubscribe_url')
                if unsubscribe_url:
                    body = body.replace('{{ unsubscribe_url }}', unsubscribe_url)

            if not email_addr:
                continue

            try:
                msg = MIMEText(body, 'html')
                msg['Subject'] = subject
                msg['From'] = from_addr
                msg['To'] = email_addr

                server.sendmail(envelope_from, [email_addr], msg.as_string())
                print(f'SMTP email sent to {email_addr}')
                success_count += 1
            except Exception as e:
                print(f'Failed to send to {email_addr}: {e}')

        server.quit()
        return success_count
    except Exception as e:
        print(f'SMTP connection failed: {e}')
        return 0
