#!/bin/bash

rm db.sqlite3
rm -rf ./helperapi/migrations
python3 manage.py migrate
python3 manage.py makemigrations helperapi
python3 manage.py migrate helperapi
python3 manage.py loaddata users
python3 manage.py loaddata tokens
python3 manage.py loaddata schools
python3 manage.py loaddata directors
python3 manage.py loaddata props
python3 manage.py loaddata uniforms
python3 manage.py loaddata music
python3 manage.py loaddata instruments
python3 manage.py loaddata students