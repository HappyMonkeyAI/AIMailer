#!/usr/bin/env python3
import json
import os
import sys
from datetime import datetime

# Add src to path
sys.path.insert(0, 'src')

def log(message):
    timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    print(f'[{timestamp}] {message}')

def main():
    try:
        import boto3
        sqs = boto3.client('sqs', region_name='us-east-1')
        queue_url = 'https://sqs.us-east-1.amazonaws.com/900211028177/aimailer-email-queue'
        
        log('Processing email queue (dry-run mode)')
        
        # Get all messages
        response = sqs.receive_message(
            QueueUrl=queue_url,
            MaxNumberOfMessages=10
        )
        
        messages = response.get('Messages', [])
        log(f'Found {len(messages)} messages in queue')
        
        for message in messages:
            body = json.loads(message['Body'])
            subject = body.get('subject', 'No subject')
            recipient = body.get('recipient', 'No recipient')
            
            log(f'📧 Would send: "{subject}" to {recipient}')
            
            # For demo, delete the message
            sqs.delete_message(
                QueueUrl=queue_url,
                ReceiptHandle=message['ReceiptHandle']
            )
            log(f'✅ Message processed and removed from queue')
            
        if not messages:
            log('No messages to process')
            
    except Exception as e:
        log(f'❌ Error: {e}')

if __name__ == '__main__':
    main()
