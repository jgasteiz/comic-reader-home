# CLAUDE.md

## Project Overview

Comic Reader Home is a Django web application for serving CBR (RAR) and CBZ (ZIP) comic files on a home network. It provides browsing, reading, progress tracking, and favorites.

## Tech Stack

- **Backend:** Django 4.0.3, Python 3.11+
- **Database:** SQLite (default) or PostgreSQL (via `USE_POSTGRES=1`)
- **Frontend:** Bootstrap, jQuery, Django templates; React 18 (vendored UMD) for the SPA reader
- **Testing:** pytest-django
- **Formatting:** black, isort
- **CI:** CircleCI

## Project Structure

```
core/               # Django project settings, URLs, WSGI
reader/             # Main Django app
  models.py         # FileItem model (comics and directories)
  views.py          # HTTP view functions
  domain/           # Business logic (no Django deps)
    _operations.py  # State changes (mark read, update status)
    _queries.py     # Read operations (page extraction, comic parsing)
  application/      # Orchestration layer
    file_items.py   # File system scanning, DB population
    read.py         # Comic page extraction coordination
  management/commands/  # populatedb, extractall
tests/              # pytest test suite
templates/reader/   # Django HTML templates
static/             # CSS, JS libraries, extracted comic pages
  js/               # Application JS (comic-reader-spa.js)
  lazylibs/         # Vendored third-party libs (Bootstrap, jQuery, React)
```

## Setup

1. Create a `.env` file in the project root:
   ```
   SECRET_KEY=your-secret-key
   COMICS_SRC_PATH=/absolute/path/to/comics
   COMICS_EXTRACT_PATH=/absolute/path/to/extraction  # optional
   ```
2. `pip install -r requirements.txt`
3. `./manage.py migrate`
4. `./manage.py populatedb`

## Common Commands

- **Run dev server:** `./manage.py runserver`
- **Populate DB from filesystem:** `./manage.py populatedb`
- **Pre-extract all comics:** `./manage.py extractall`
- **Run tests:** `pytest`
- **Format code:** `black <file>` and `isort <file>`

## Testing

Tests live in `tests/`. Run with `pytest`. The test settings module is `tests.settings` (configured in `pytest.ini`). Tests use a fixture CBZ file at `tests/fixtures/comics/`. The `--reuse-db` flag is enabled by default for faster reruns.

## Architecture Notes

- **Layered architecture:** Views call into `domain/` and `application/` layers. Domain functions contain pure business logic with no Django dependencies. Application functions orchestrate domain logic with framework concerns.
- **Single model:** `FileItem` represents both directories and comics (distinguished by `file_type` field). Uses a self-referential `parent` FK for hierarchy.
- **Comic formats:** CBR handled via `rarfile`, CBZ via `zipfile`. Pages are extracted on-demand to `COMICS_EXTRACT_PATH/{comic_id}/` and cached for subsequent views.
- **SPA reader:** A React-based single-page reader at `/comic/<id>/spa/` loads comic metadata as JSON and navigates pages client-side (no full reloads). Uses `React.createElement` directly (no JSX/Babel). Progress is tracked via a POST endpoint at `/comic/<id>/progress/`. The original server-rendered reader at `/comic/<id>/` is still available.

## Environment Variables

| Variable | Required | Description |
|---|---|---|
| `SECRET_KEY` | Yes | Django secret key (defaults to "1234" if unset) |
| `COMICS_SRC_PATH` | Yes | Absolute path to directory with CBR/CBZ files |
| `COMICS_EXTRACT_PATH` | No | Where extracted pages are stored (defaults to `static/comics/tmp`) |
| `USE_POSTGRES` | No | Set to "1" to use PostgreSQL |
| `DATABASE_HOST` | No | PostgreSQL host (default: localhost) |
| `DATABASE_NAME` | No | PostgreSQL database (default: comics) |
| `DATABASE_USER` | No | PostgreSQL user (default: postgres) |
| `DATABASE_PASSWORD` | No | PostgreSQL password (default: postgres) |
| `DATABASE_PORT` | No | PostgreSQL port (default: 5432) |
