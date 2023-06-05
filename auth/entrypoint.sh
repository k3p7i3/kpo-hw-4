#!/bin/sh

echo "Waiting for postgres..."
while ! nc -z auth-db 5432; do
    sleep 0.1
done
echo "PostgreSQL started"

cd ./auth
alembic upgrade head
cd ../

exec "$@"