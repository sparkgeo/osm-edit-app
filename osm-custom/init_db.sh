#!/bin/bash
set -ex

echo "Start DB INIT"

# Wait until Postgres is ready
until psql -U postgres -c '\l'; do
  echo >&2 "Postgres is unavailable - sleeping"
  sleep 1
done
echo >&2 "Postgres is up - continuing"

# Check if the script has already run.
if psql -U postgres-tAc "SELECT 1 FROM pg_roles WHERE rolname='openstreetmap'"; then
  echo "User does NOT exist"

  # Password and superuser privilege are needed to successfully run test suite
  psql -v ON_ERROR_STOP=0 -U postgres -c "CREATE USER openstreetmap SUPERUSER PASSWORD 'openstreetmap';"
  psql -v ON_ERROR_STOP=0 -U postgres -c "GRANT ALL PRIVILEGES ON DATABASE openstreetmap TO openstreetmap;"

  # Create btree_gist extensions
  psql -v ON_ERROR_STOP=0 -c "CREATE EXTENSION btree_gist" openstreetmap

  # Define custom functions
  psql -v ON_ERROR_STOP=0 -f "/app/config/osm-db-functions.sql" openstreetmap

else
  echo "User exists, skipping init"
fi

echo "Done DB INIT"

exec ${@}