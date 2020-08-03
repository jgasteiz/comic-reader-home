VENV ?= ./env

migrate:
	docker-compose run comics python manage.py migrate

populatedb:
	docker-compose run comics python manage.py populatedb
