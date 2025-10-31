#!/usr/bin/env bash
# Exit on error
set -o errexit

# Modify this line as needed for your package manager (pip, poetry, etc.)
pip install -r requirements.txt

# Change to the Django project directory
cd veterinaria_project

# Convert static asset files
python manage.py collectstatic --no-input

# Apply any outstanding database migrations
python manage.py migrate

# Wait a moment for database to be ready
sleep 5

# Load data from fixtures if available
if [ -f "db_dump.json" ]; then
    echo "Loading data from fixtures..."
    python manage.py loaddata db_dump.json
fi

# Run population script if available
if [ -f "populate_db.py" ]; then
    echo "Running database population script..."
    python populate_db.py
fi