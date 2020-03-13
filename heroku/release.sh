set -e

# See https://github.com/niteoweb/pyramid-realworld-example-app/issues/86
# echo "Installing required extensions"
# psql $DATABASE_URL -c "CREATE EXTENSION IF NOT EXISTS pgcrypto;"

echo "Running database migrations"

alembic -c production.ini -x url=$DATABASE_URL upgrade head || echo "Database migrations failed!"

echo "Done"
