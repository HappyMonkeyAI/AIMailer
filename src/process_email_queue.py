#!/usr/bin/env python3
import json
import os
import sys
import time
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from datetime import datetime

# Add src to path for imports
sys.path.insert(0, os.path.dirname(__file__))

SQS_QUEUE_URL = os.environ.get('SQS_QUEUE_URL', 'https://sqs.us-east-1.amazonaws.com/900211028177/aimailer-email-queue')
AWS_REGION = os.environ.get('AWS_REGION', 'us-east-1')
SMTP_HOST = os.environ.get('SMTP_HOST', 'smtp.gmail.com')
SMTP_PORT = int(os.environ.get('SMTP_PORT', 587))
SMTP_USER = os.environ.get('SMTP_USER')
SMTP_PASS = os.environ.get('SMTP_PASS')


def log(message):
    """Simple logging with timestamp."""
    timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    print(f'[{timestamp}] {message}')


def send_via_smtp(subject, html_body, recipient, sender):
    """Send via SMTP."""
    try:
        if not SMTP_HOST or not SMTP_USER:
            log('SMTP not configured - skipping email delivery')
            return False
            
        msg = MIMEMultipart('alternative')
        msg['Subject'] = subject
        msg['From'] = sender
        msg['To'] = recipient
        msg.attach(MIMEText(html_body, 'html'))
        
        server = smtplib.SMTP(SMTP_HOST, SMTP_PORT)
        server.starttls()
        if SMTP_PASS:
            server.login(SMTP_USER, SMTP_PASS)
        server.sendmail(sender, [recipient], msg.as_string())
        server.quit()
        log(f'✅ SMTP email sent to {recipient}')
        return True
    except Exception as e:
        log(f'❌ SMTP failed: {e}')
        return False


def process_message(message_body):
    """Process a single email message."""
    try:
        data = json.loads(message_body)
        subject = data.get('subject', 'AIMailer')
        html_body = data.get('html_body', '')
        recipient = data.get('recipient', '')
        sender = data.get('sender', SMTP_USER or 'aimailer@sparktsl.com')
        
        log(f'Processing email: "{subject}" to {recipient}')
        
        # For now, just use SMTP since SES access is restricted
        if send_via_smtp(subject, html_body, recipient, sender):
            return True
        else:
            log(f'❌ Failed to send email to {recipient}')
            return False
    except Exception as e:
        log(f'❌ Error processing message: {e}')
        return False


def main():
    """Main processor loop."""
    try:
        import boto3
        sqs = boto3.client('sqs', region_name=AWS_REGION)
        
        log(f'Starting email processor for queue: {SQS_QUEUE_URL}')
        log(f'SMTP configured: {bool(SMTP_HOST and SMTP_USER)}')
        
        processed_count = 0
        
        while True:
            try:
                # Poll for messages
                response = sqs.receive_message(
                    QueueUrl=SQS_QUEUE_URL,
                    MaxNumberOfMessages=5,
                    WaitTimeSeconds=20  # Long polling
                )
                
                messages = response.get('Messages', [])
                if not messages:
                    log('No messages, waiting...')
                    continue
                    
                for message in messages:
                    message_id = message['MessageId']
                    receipt_handle = message['ReceiptHandle']
                    body = message['Body']
                    
                    if process_message(body):
                        # Delete message on success
                        sqs.delete_message(
                            QueueUrl=SQS_QUEUE_URL,
                            ReceiptHandle=receipt_handle
                        )
                        processed_count += 1
                        log(f'✅ Message {message_id} processed and deleted (total: {processed_count})')
                    else:
                        log(f'❌ Message {message_id} failed, leaving in queue')
                        
            except Exception as e:
                log(f'❌ Polling error: {e}')
                time.sleep(30)  # Wait before retrying
                    
    except KeyboardInterrupt:
        log('Processor stopped by user')
    except Exception as e:
        log(f'❌ Processor error: {e}')


if __name__ == '__main__':
    main()
