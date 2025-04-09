#!/bin/bash
set -e

cd /workspace/backend

# Attendre que la base de données soit prête
echo "Waiting for database to be ready..."
sleep 5

# Exécuter les migrations Alembic
echo "Running database migrations..."
alembic upgrade head

# Démarrer l'application
echo "Starting application..."
exec uvicorn app.main:app --reload --workers 1 --host 0.0.0.0 --port 8000