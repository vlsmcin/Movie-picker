#!/bin/sh
set -e

echo "Waiting for database..."

until pg_isready -h "$DB_HOST" -p "$DB_PORT" -U "$DB_USER"; do
  sleep 1
done

echo "Database is ready!"

python manage.py makemigrations
python manage.py migrate
python manage.py fill_genres

exec "$@"
