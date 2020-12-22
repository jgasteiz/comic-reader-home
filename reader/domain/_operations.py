from reader import models
from reader.domain import _queries


def update_comic_status(comic: models.FileItem, page_number: int):
    comic.set_furthest_read_page(page_number)
    num_pages = _queries.get_num_pages(comic)
    # If we've reached the end, mark the comic as finished.
    if page_number == num_pages - 1:
        comic.mark_as_read()


def mark_directory_comics_as_read(directory: models.FileItem):
    for comic in models.FileItem.objects.filter(
        parent=directory, file_type=models.FileItem.COMIC
    ):
        comic.mark_as_read()


def get_or_create_file_item(path: str, parent: models.FileItem) -> models.FileItem:
    """
    Create or retrieve an existing file for a given path and parent.
    """
    file_item, _ = models.FileItem.objects.get_or_create(path=path, parent=parent)
    file_item.set_name()
    file_item.set_file_type()
    return file_item
