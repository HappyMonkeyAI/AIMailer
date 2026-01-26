#!/bin/bash
# Quick start script for AIMailer Web Control Panel

cd "$(dirname "$0")"

echo "🚀 Starting AIMailer Web Control Panel..."
echo ""

# Activate virtual environment
source venv/bin/activate

# Check if migrations are needed
echo "📊 Checking for pending migrations..."
python manage.py makemigrations --check --dry-run 2>/dev/null
if [ $? -ne 0 ]; then
    echo "⚠️  Migrations needed. Running migrations..."
    python manage.py migrate
fi

# Start the development server
echo ""
echo "✅ Starting Django development server on http://localhost:8001"
echo "📝 Admin panel: http://localhost:8001/admin"
echo ""
echo "Press CTRL+C to stop the server"
echo ""

python manage.py runserver 0.0.0.0:8001
