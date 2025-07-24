#!/bin/bash

set -e

echo "cur dir: " $(pwd)

ls -l

python manage.py collectstatic

python manage.py migrate

python manage.py runserver 0.0.0.0:8000
