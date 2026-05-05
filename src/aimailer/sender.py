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
               sender_email: str = None, sender_name: str = None, 
               custom_smtp_host: str = None, custom_smtp_port: int = None,
               custom_smtp_user: str = None, custom_smtp_pass: str = None,
               custom_use_tls: bool = None) -> int:
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

    # Determine which SMTP credentials to use
    host = custom_smtp_host or SMTP_HOST
    port = custom_smtp_port or SMTP_PORT
    user = custom_smtp_user if custom_smtp_user is not None else SMTP_USER
    password = custom_smtp_pass if custom_smtp_pass is not None else SMTP_PASS
    
    # Require SMTP host and credentials
    if not host:
        raise RuntimeError('SMTP Host not configured (neither custom nor default)')

    try:
        # TLS handling logic
        use_ssl = False
        if custom_use_tls is False and port == 465:
             # This is a bit of a conflict (port 465 is implicit SSL), but we'll respect the port
             use_ssl = True
        elif port == 465:
             use_ssl = True
             
        if use_ssl:
            server = smtplib.SMTP_SSL(host, port)
        else:
            server = smtplib.SMTP(host, port)
            
            # Use TLS if explicitly requested or if it's the global default (and not port 465)
            # Standard behaviour is to use TLS on ports like 587
            should_use_tls = custom_use_tls if custom_use_tls is not None else True
            if should_use_tls:
                server.starttls()
            
        if user and password:
            server.login(user, password)

        # Determine From address
        from_addr = sender_email or user or 'no-reply@example.com'
        if sender_name:
            # Sanitize sender_name to prevent header injection
            clean_name = sender_name.replace('\n', '').replace('\r', '').strip()
            from_addr = f"{clean_name} <{from_addr}>"

        success_count = 0
        envelope_from = user or sender_email or 'no-reply@example.com'

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
