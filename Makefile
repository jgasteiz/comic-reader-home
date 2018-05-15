VENV ?= ./env

install:
	python3 -m venv $(VENV) && \
	$(VENV)/bin/pip install -r requirements/local.txt

migrate:
	$(VENV)/bin/python3 manage.py migrate

loaddata:
	$(VENV)/bin/python3 manage.py populatedb

serve:
	$(VENV)/bin/python manage.py runserver

servewithyarn:
	$(VENV)/bin/python manage.py yarnrunserver

test:
	$(VENV)/bin/pytest

dockerbuild:
	docker-compose up --build

dockerstop:
	docker-compose down

dockerserve:
	docker-compose up web
