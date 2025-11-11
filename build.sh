#!/bin/bash
set -e

echo "Installing dependencies..."
pip install -r requirements.txt

echo "Collecting static files..."
python3 manage.py collectstatic --noinput

echo "Build complete!"
