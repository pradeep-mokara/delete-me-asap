#!/bin/bash
set -e

echo "⏳ Waiting for Postgres at $POSTGRES_HOST:$POSTGRES_PORT..."

until pg_isready -h "$POSTGRES_HOST" -p "$POSTGRES_PORT" -U "$POSTGRES_USER" -d "$POSTGRES_DB"; do
  echo "Waiting for postgres..."
  sleep 1
done


echo "✅ Postgres is up"

