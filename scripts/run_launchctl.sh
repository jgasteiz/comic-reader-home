#!/usr/bin/env bash

cd $HOME/Developer/comic-reader/
source ./env/bin/activate

gunicorn --bind 0.0.0.0:8080 comicreader.wsgi:application &
celery -A reader.tasks worker --loglevel=info --concurrency=2 &
