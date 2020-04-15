createdb:
	docker-compose run db createdb -U postgres "comics"

migrate:
	docker-compose up &
	docker-compose run web python manage.py migrate
	docker-compose run web python manage.py populatedb
	docker-compose down


VENV ?= ./env

local_install:
	python3 -m venv $(VENV) && \
	$(VENV)/bin/pip install -r requirements.txt && \
	yarn install

local_migrate:
	$(VENV)/bin/python3 manage.py migrate

local_populatedb:
	$(VENV)/bin/python3 manage.py populatedb

local_build:
	yarn webpack

local_watch:
	yarn webpack-watch

local_serve:
	$(VENV)/bin/python manage.py runserver 0.0.0.0:8000

local_test:
	$(VENV)/bin/pytest ${ARGS}
