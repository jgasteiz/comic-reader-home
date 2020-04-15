VENV ?= ./env

install:
	python3 -m venv $(VENV) && \
	$(VENV)/bin/pip install -r requirements.txt && \
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
	$(VENV)/bin/python manage.py runserver 0.0.0.0:8000

test:
	$(VENV)/bin/pytest ${ARGS}
