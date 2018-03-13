import os
import django
from celery import Celery

# set the default Django settings module for the 'celery' program.
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "comicreader.local_settings")
# Setup django project
django.setup()

app = Celery('tasks', broker='pyamqp://guest@localhost//')


@app.task
def extract_comic_file(comic_path):
    from reader.utils import Comic
    comic = Comic(comic_path)
    comic.extract_all_pages()
    return 'Comic file extracted'
