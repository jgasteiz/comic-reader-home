# Comic Reader Home

[![circle ci status](https://circleci.com/gh/jgasteiz/comic-reader-home.svg?style=shield&circle-token=:circle-token)](https://circleci.com/gh/jgasteiz/comic-reader-home/tree/master)

This is an app to serve my cbr and cbz comic files on my home network.

## How to get this running

1. Create an `.env` file in the project root with the following contents:
```dotenv
SECRET_KEY=123456  # replace with something else
COMICS_ROOT=~/Data/comics  # absolute path to a directory with cbr/cbz files.
POSTGRES_DATA_PATH=~/Data/pg-data  # absolute path where the postgres db can store its data files.
```
2. Run `docker-compose up` to setup the docker containers and run them.
3. On a separate window, run `docker-compose run comics python manage.py migrate`
   to initialise the database and `docker-compose run comics python manage.py populatedb`
   to load the comic files into the database.
4. The server should be now up and running in http://localhost:8080/.
