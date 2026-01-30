#!/bin/bash

echo "Personal Finance Tracker - Setup Script"
echo "========================================"

echo "Creating virtual environment..."
python -m venv venv

echo "Activating virtual environment..."
source venv/Scripts/activate

echo "Installing dependencies..."
pip install -r requirements.txt

echo "Running migrations..."
python manage.py migrate

echo "Creating superuser..."
python manage.py createsuperuser

echo "Setup complete! Run 'python manage.py runserver' to start the application."
