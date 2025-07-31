#!/bin/bash

set -e

echo "cur dir: " $(pwd)

python manage.py collectstatic --noinput
python manage.py migrate
python manage.py runserver 0.0.0.0:8000
