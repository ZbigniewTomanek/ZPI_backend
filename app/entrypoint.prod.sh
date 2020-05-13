#!/bin/sh

if [ "$DATABASE" = "postgres" ]
then
    echo "Waiting for postgres..."

    while ! nc -z "$SQL_HOST" "$SQL_PORT"; do
      sleep 0.1
    done

    echo "PostgreSQL started"
fi

python manage.py collectstatic --no-input --clear
python manage.py makemigrations backend
python manage.py migrate
echo "from backend.populate_db import init_system; init_system()" | python manage.py shell


exec "$@"