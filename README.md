# Comic Reader Home

[![circle ci status](https://circleci.com/gh/jgasteiz/comic-reader-home.svg?style=shield&circle-token=:circle-token)](https://circleci.com/gh/jgasteiz/comic-reader-home/tree/master)

This is an app to serve my cbr and cbz comic files on my home network.

## How to get this running

1. Create an `.env` file in the project root with the following contents:
```dotenv
# Replace with something else
SECRET_KEY=123456
# Absolute path to a directory with cbr/cbz files.
COMICS_SRC_PATH=/Users/javi.manzano/Data/comics
# Absolute path where comics should be extracted.
COMIC_EXTRACT_PATH=/Users/javi.manzano/Data/comics-extracted
```
2. Run the following commands:
```shell
./manage.py migrate
./manage.py populatedb
./manage.py runserver
```
