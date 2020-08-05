from zipfile import ZipFile

from django.core.cache import cache

from rarfile import RarFile
from reader import models


def get_num_pages(comic: models.FileItem) -> int:
    cache_key = f"num_pages_{comic.pk}"
    if cache.get(cache_key):
        return cache.get(cache_key)

    if comic.file_type == comic.COMIC:
        # Initialise the cb_file. This will raise a FileNotFoundError if
        # zipfile/rarfile can't find the file.
        if comic.name.endswith(".cbz"):
            comic.cb_file = ZipFile(comic.path)
        else:
            comic.cb_file = RarFile(comic.path)

        # Set all the page names in order
        all_pages = [
            p
            for p in comic.cb_file.namelist()
            if p.endswith(".jpg") or p.endswith(".jpeg") or p.endswith(".png")
        ]
        # Remove hidden files (files that start with `.`) from the pages list.
        all_pages = list(
            filter(lambda x: not x.split("/")[-1].startswith("."), all_pages)
        )
        num_pages = len(all_pages)
    else:
        num_pages = 0

    cache.set(cache_key, num_pages)
    return num_pages
