from .settings import *

SECRET_KEY = '123456'

COMIC_EXTRACT_PATH = os.path.join(BASE_DIR, 'static/comics/tmp')
COMICS_ROOT = os.path.join(BASE_DIR, 'comicreader/tests_fixtures/comics')
STATIC_ROOT = ''
USE_CELERY = False
