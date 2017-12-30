from zipfile import ZipFile

from celery import Celery
from rarfile import RarFile

app = Celery('tasks', broker='pyamqp://guest@localhost//')


@app.task
def extract_comic_file(decoded_comic_path, destination):
    # Create a zip or a rar file depending on the comic file type.
    if decoded_comic_path.endswith('.cbz'):
        cb_file = ZipFile(decoded_comic_path)
    else:
        cb_file = RarFile(decoded_comic_path)

    cb_file.extractall(destination)
    return 'Comic file extracted'
