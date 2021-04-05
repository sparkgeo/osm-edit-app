#!/bin/bash
set -x

echo "Start DB INIT"

# Wait until Postgres is ready
until psql -c '\l' postgres; do
  echo >&2 "Postgres is unavailable - sleeping"
  sleep 1
done
echo >&2 "Postgres is up - continuing"

# Create the database
psql -v ON_ERROR_STOP=1 -c "CREATE DATABASE openstreetmap;" postgres

# Password and superuser privilege are needed to successfully run test suite
psql -c "CREATE USER openstreetmap PASSWORD 'openstreetmap';"
psql -c "GRANT ALL PRIVILEGES ON DATABASE openstreetmap TO openstreetmap;"

# Create btree_gist extensions
psql -c "CREATE EXTENSION btree_gist;"

# Define custom functions
psql -f "/app/config/osm-db-functions.sql"

echo "Done DB INIT"

echo "Run Migrations"
bundle exec rake db:migrate

echo "Seed DB"
rails db:seed

exec ${@}