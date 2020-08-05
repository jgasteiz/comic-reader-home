from core.settings import *

SECRET_KEY = "123456"
DEBUG = False

COMICS_ROOT = os.path.join(BASE_DIR, "tests/fixtures/comics")

DATABASES["default"] = {
    "ENGINE": "django.db.backends.sqlite3",
    "NAME": os.path.join(BASE_DIR, "db.sqlite3"),
}
