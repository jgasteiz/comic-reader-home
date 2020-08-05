VENV ?= ./env

makemigrations:
	docker-compose run comics python manage.py makemigrations

migrate:
	docker-compose run comics python manage.py migrate

populatedb:
	docker-compose run comics python manage.py populatedb

extracteverything:
	docker-compose run comics python manage.py extracteverything
