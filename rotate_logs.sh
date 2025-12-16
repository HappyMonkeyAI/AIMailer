#!/bin/bash
# Simple log rotation for AIMailer

LOG_DIR="/var/www/html/happymonkey.ai/AIMailer"
MAX_SIZE="10M"  # Rotate when logs exceed 10MB
KEEP_DAYS=30    # Keep logs for 30 days

# Function to rotate a log file
rotate_log() {
    local logfile="$1"
    local basename=$(basename "$logfile" .log)
    
    if [ -f "$logfile" ] && [ $(stat -f%z "$logfile" 2>/dev/null || stat -c%s "$logfile" 2>/dev/null) -gt 10485760 ]; then
        # Create timestamped backup
        timestamp=$(date +%Y%m%d_%H%M%S)
        mv "$logfile" "${logfile}.${timestamp}"
        
        # Compress old log
        gzip "${logfile}.${timestamp}"
        
        # Create new empty log
        touch "$logfile"
        
        echo "Rotated $logfile"
    fi
}

# Rotate logs if they're too big
rotate_log "$LOG_DIR/aimailer.log"
rotate_log "$LOG_DIR/processor.log"
rotate_log "$LOG_DIR/run_processor.log"
rotate_log "$LOG_DIR/rotation.log"

# Clean up old compressed logs (older than 30 days)
find "$LOG_DIR" -name "*.log.*.gz" -mtime +$KEEP_DAYS -delete

echo "Log rotation complete"
