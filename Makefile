VENV ?= ./env

install:
	python3 -m venv $(VENV) && \
	$(VENV)/bin/pip install -r requirements.txt

migrate:
	$(VENV)/bin/python3 manage.py migrate

serve:
	yarn run webpack && \
	$(VENV)/bin/python3 manage.py runserver

servewithyarn:
	$(VENV)/bin/python3 manage.py yarnrunserver

test:
	$(VENV)/bin/pytest

dockertest:
	docker-compose run --rm web python manage.py test --settings=comicreader.test_settings

dockerstop:
	docker-compose down

dockerserve:
	docker-compose up web
