from .settings import *

# Set an actual secret key.
SECRET_KEY = os.environ.get('SECRET_KEY')

DEFAULT_COMIC_EXTRACT_PATH = os.path.join(BASE_DIR, 'static/comics/tmp')
COMIC_EXTRACT_PATH = os.environ.get('COMIC_EXTRACT_PATH', DEFAULT_COMIC_EXTRACT_PATH)
if os.environ.get('USE_DOCKER') == 'true':
    COMICS_ROOT = '/comics'
else:
    COMICS_ROOT = os.environ.get('COMICS_ROOT')
STATIC_ROOT = ''
