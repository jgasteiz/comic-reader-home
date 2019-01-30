VENV ?= ./env

install:
	python3 -m venv $(VENV) && \
	$(VENV)/bin/pip install -r requirements/local.txt && \
	yarn install

migrate:
	$(VENV)/bin/python3 manage.py migrate

populatedb:
	$(VENV)/bin/python3 manage.py populatedb

build:
	yarn webpack

watch:
	yarn webpack-watch

serve:
	$(VENV)/bin/python manage.py runserver

test:
	$(VENV)/bin/pytest ${ARGS}

dockerbuild:
	docker-compose up --build

dockerstop:
	docker-compose down

dockerserve:
	docker-compose up web
