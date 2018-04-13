# Comic Reader Home

[![circle ci status](https://circleci.com/gh/jgasteiz/comic-reader-home.svg?style=shield&circle-token=:circle-token)](https://circleci.com/gh/jgasteiz/comic-reader-home/tree/master)

This is an app to serve my cbr and cbz comic files on my home network.

## How to get this running

1. Copy `comicreader/local_settings.py.example` to `comicreader/local_settings.py`.
2. Set a value for `SECRET_KEY`: any string realy, just type some random combination of numbers and letters.
3. Set a value for `COMICS_ROOT`: this should be the absolute path in your server where your `.cbr` and `.cbz` files live.
4. Create a virtualenv and install the python3 dependencies:
  4.1. On the project root: `python3 -m venv env`
  4.2. `source ./env/bin/activate`
  4.1. `pip install -r requirements.txt`
5. Make sure yarn or npm are installed globally: `npm -g install yarn`
6. Install FE dependencies: `yarn install`
7. Build FE dependencies: `yarn run webpack`
8. Run the project: `./manage.py runserver`
