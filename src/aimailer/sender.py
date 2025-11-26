import os
import json
import smtplib
from email.mime.text import MIMEText
from typing import List, Union

SMTP_HOST = os.environ.get('SMTP_HOST')
SMTP_PORT = int(os.environ.get('SMTP_PORT', 587)) if os.environ.get('SMTP_PORT') else None
SMTP_USER = os.environ.get('SMTP_USER')
SMTP_PASS = os.environ.get('SMTP_PASS')
SQS_QUEUE_URL = os.environ.get('SQS_QUEUE_URL', 'https://sqs.us-east-1.amazonaws.com/900211028177/aimailer-email-queue')
AWS_REGION = os.environ.get('AWS_REGION', 'us-east-1')


def send_via_sqs(subject: str, html_body: str, recipients: Union[str, List[str]]) -> bool:
    """Send email via AWS SQS queue for processing."""
    try:
        import boto3
        sqs = boto3.client('sqs', region_name=AWS_REGION)
        
        # Ensure recipients is a list
        if isinstance(recipients, str):
            recipients = [recipients]
        
        # Queue separate message for each recipient
        success_count = 0
        for recipient in recipients:
            message = {
                'subject': subject,
                'html_body': html_body,
                'recipient': recipient,
                'sender': SMTP_USER or 'aimailer@sparktsl.com',
                'timestamp': str(os.environ.get('CURRENT_TIME', ''))
            }
            
            response = sqs.send_message(
                QueueUrl=SQS_QUEUE_URL,
                MessageBody=json.dumps(message)
            )
            print(f'Email queued to SQS for {recipient}: {response["MessageId"]}')
            success_count += 1
        
        return success_count == len(recipients)
    except Exception as e:
        print(f'SQS send failed: {e}')
        return False


def send_email(subject: str, html_body: str, recipients: Union[str, List[str]], dry_run: bool = True) -> bool:
    """Send HTML email to multiple recipients. If dry_run is True, only print action and do not send."""
    print('send_email called; dry_run=', dry_run)
    
    # Ensure recipients is a list
    if isinstance(recipients, str):
        recipients = [recipients]
    
    if dry_run:
        print(f'DRY RUN: would send email to {len(recipients)} recipients: {", ".join(recipients)}')
        return True
    
    # Try SQS first if available
    if SQS_QUEUE_URL:
        return send_via_sqs(subject, html_body, recipients)
    
    # Fallback to SMTP
    if not SMTP_HOST:
        raise RuntimeError('Neither SQS_QUEUE_URL nor SMTP_HOST configured')
    
    try:
        server = smtplib.SMTP(SMTP_HOST, SMTP_PORT or 587)
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
