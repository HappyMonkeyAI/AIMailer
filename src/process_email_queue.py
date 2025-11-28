#!/usr/bin/env python3
import os
import time
from datetime import datetime

# Simple SMTP-only processor placeholder
SMTP_HOST = os.environ.get('SMTP_HOST')
SMTP_USER = os.environ.get('SMTP_USER')
SMTP_PASS = os.environ.get('SMTP_PASS')


def log(message):
    timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    print(f'[{timestamp}] {message}')


def main():
    """Run a lightweight idle processor for SMTP-only deployments.

    Note: SQS/SES support has been removed. This process exists so the
    systemd unit can remain active without attempting to talk to AWS.
    """
    try:
        log('Starting SMTP-only processor (SQS/SES support removed)')
        log(f'SMTP configured: {bool(SMTP_HOST and SMTP_USER)}')

        # Keep the service alive; the run pipeline sends emails directly via SMTP.
        while True:
            log('Processor running in SMTP-only mode; no queue polling.')
            time.sleep(60)

    except KeyboardInterrupt:
        log('Processor stopped by user')
    except Exception as e:
        log(f'❌ Processor error: {e}')


if __name__ == '__main__':
    main()
