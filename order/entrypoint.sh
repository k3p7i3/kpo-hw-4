#!/bin/sh

echo "Waiting for postgres..."
while ! nc -z order-db 5432; do
    sleep 0.1
done
echo "PostgreSQL started"

cd ./order
alembic upgrade head
cd ../

exec "$@"