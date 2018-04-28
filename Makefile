VENV ?= ./env

install:
	python3 -m venv $(VENV) && \
	$(VENV)/bin/pip install -r requirements.txt

migrate:
	$(VENV)/bin/python3 manage.py migrate

serve:
	$(VENV)/bin/python3 manage.py yarnrunserver

servenoyarn:
	$(VENV)/bin/python3 manage.py runserver

test:
	$(VENV)/bin/python3 manage.py test --settings=comicreader.test_settings

dockertest:
	docker-compose run --rm web python manage.py test --settings=comicreader.test_settings

dockerstop:
	docker-compose down

dockerserve:
	docker-compose up web
