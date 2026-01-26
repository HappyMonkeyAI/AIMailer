#!/bin/bash

# Function to wait for a service to be ready
wait_for_service() {
    local host="$1"
    local port="$2"
    local service="$3"
    
    echo "Waiting for $service ($host:$port)..."
    while ! nc -z "$host" "$port"; do
      sleep 1
    done
    echo "$service is up!"
}

# Wait for database if host is provided
if [ -n "$DB_HOST" ]; then
    wait_for_service "$DB_HOST" "${DB_PORT:-5432}" "Database"
fi

# Wait for Redis if url is provided
if [ -n "$REDIS_URL" ]; then
    # Extract host and port from REDIS_URL (simplified)
    # redis://redis:6379/0 -> redis 6379
    REDIS_HOST=$(echo $REDIS_URL | sed -e 's|.*//\(.*\):.*|\1|')
    REDIS_PORT=$(echo $REDIS_URL | sed -e 's|.*:\(.*\)/.*|\1|')
    wait_for_service "$REDIS_HOST" "${REDIS_PORT:-6379}" "Redis"
fi

# Apply database migrations
if [[ "$*" == *"runserver"* ]]; then
    echo "Applying database migrations..."
    python manage.py migrate --noinput
    
    echo "Collecting static files..."
    python manage.py collectstatic --noinput
fi

# Run the command passed to the container
exec "$@"
