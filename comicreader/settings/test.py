from .common import *

SECRET_KEY = "123456"
DEBUG = False

COMIC_EXTRACT_PATH = os.path.join(BASE_DIR, "static/comics/tmp")
COMICS_ROOT = os.path.join(BASE_DIR, "comicreader/tests_fixtures/comics")

DATABASES["default"] = {
    "ENGINE": "django.db.backends.sqlite3",
    "NAME": os.path.join(BASE_DIR, "db.sqlite3"),
}
