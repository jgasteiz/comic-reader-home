# Comic Reader Home

[![circle ci status](https://circleci.com/gh/jgasteiz/comic-reader-home.svg?style=shield&circle-token=:circle-token)](https://circleci.com/gh/jgasteiz/comic-reader-home/tree/master)

This is an app to serve my cbr and cbz comic files on my home network.

## How to get this running

1. Copy `.env.example` to `.env`.
2. Set values for both SECRET_KEY and COMICS_ROOT environment variables.
3. Install dependencies and activate the virtualenv:
  3.1. On the project root: `make install`
  3.2. `source ./env/bin/activate`
4. Make sure yarn or npm are installed globally: `npm -g install yarn`
5. Install FE dependencies: `yarn install`
6. Run the db migrations: `make migrate`
7. Run the project with a watcher for static files: `make serve`

## How to get this running - with docker

1. Copy `.env.example` to `.env`.
2. Set values for both SECRET_KEY and COMICS_ROOT environment variables.
3. Run the tests: `make dockertest`
4. Serve the project: `make dockerserve`
