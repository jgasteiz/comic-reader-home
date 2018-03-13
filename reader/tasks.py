from celery import Celery

from reader.utils import Comic

app = Celery('tasks', broker='pyamqp://guest@localhost//')


@app.task
def extract_comic_file(comic_path):
    comic = Comic(comic_path)
    comic.extract_all_pages()
    return 'Comic file extracted'
