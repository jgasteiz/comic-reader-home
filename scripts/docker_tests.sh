#!/usr/bin/env bash

docker-compose run --rm web python manage.py test --settings=comicreader.test_settings
