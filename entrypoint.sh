#!/bin/sh
set -e

echo "Waiting for database..."

until alembic current >/dev/null 2>&1; do
  echo "Database not ready, retrying..."
  sleep 2
done

echo "Running Alembic migrations..."
alembic upgrade head

echo "Starting FastAPI..."
exec uvicorn app.main:app --host 0.0.0.0 --port 8000 --http h11
