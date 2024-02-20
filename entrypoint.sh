#!/bin/bash

echo "Making xss_app migrations"
python manage.py makemigrations xss_app

# Apply database migrations
echo "Applying database migrations..."
python manage.py migrate

# Load initial data
echo "Loading initial data..."
python manage.py loaddata populate.json

# Start server
echo "Starting server..."
python manage.py runserver 0.0.0.0:8000
