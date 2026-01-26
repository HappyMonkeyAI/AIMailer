#!/bin/bash
# Script to create a Django superuser for admin access

cd "$(dirname "$0")"

echo "👤 Creating Django superuser..."
echo ""

# Activate virtual environment
source venv/bin/activate

# Create superuser
python manage.py createsuperuser

echo ""
echo "✅ Superuser created successfully!"
echo "🔗 Access admin panel at: http://localhost:8001/admin"
