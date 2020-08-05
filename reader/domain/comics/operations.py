from reader import models

from . import queries


def update_comic_status(comic: models.FileItem, page_number: int):
    comic.set_furthest_read_page(page_number)
    num_pages = queries.get_num_pages(comic)
    # If we've reached the end, mark the comic as finished.
    if page_number == num_pages - 1:
        comic.mark_as_read()
