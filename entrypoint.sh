#!/bin/bash

# Apply database migrations
echo "Applying migrations..."
python manage.py migrate

# Collect static files (if needed)
echo "Collecting static files..."
python manage.py collectstatic --noinput

export PGPASSWORD="admin"
until psql -h db -U ziko -d shopdjango -c '\q'; do
  echo "Postgres is unavailable - sleeping"
  sleep 1
done

echo "Postgres is up - executing command"
exec "$@"

# Start the Django server
echo "Starting server..."
exec "$@"
