#!/bin/sh
# Used to check if Postgres is healthy before running migrations

if [ "$DATABASE" = "postgres" ]
then
    echo "Waiting for postgres..."

    while ! nc -z $SQL_HOST $SQL_PORT; do
      sleep 0.1
    done

    echo "PostgreSQL started with $SQL_HOST"
fi

# Comment this if we dont want to always migrate
python manage.py flush --no-input
python manage.py migrate

exec "$@"