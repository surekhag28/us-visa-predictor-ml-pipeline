#!/bin/sh

# Wait for the database to be ready
while ! pg_isready -h db -p 5432 -U postgres; do
  echo "Waiting for database..."
  sleep 2
done

python src/load_data/create_schema.py

dvc repro