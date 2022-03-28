import os

from django.conf import settings
from reader import domain, models


def delete_old_items():
    """
    Delete all FileItems which paths don't exist anymore.
    """
    for file_item in models.FileItem.objects.iterator():
        if not os.path.exists(file_item.path):
            print("Deleting %s" % file_item.name)
            file_item.delete()


def populate_db_from_path(path=settings.COMICS_SRC_PATH, parent=None):
    file_item = domain.get_or_create_file_item(path=path, parent=parent)

    # Start creating FileItem recursively.
    for path_name in os.listdir(path):
        # Skip hidden files/directories.
        if path_name.startswith("."):
            continue

        child_path = os.path.join(path, path_name)

        # If the child is a directory, call populate_db_from_path with its path.
        if os.path.isdir(child_path):
            populate_db_from_path(path=child_path, parent=file_item)
        # If it's a comic, simply create the file item.
        elif domain.is_file_name_comic_file(path_name):
            domain.get_or_create_file_item(path=child_path, parent=file_item)


def extract_all_comics():
    """
    Extract all comics that haven't been extracted yet.
    """
    for comic in models.FileItem.objects.comics().iterator():
        cb_file = domain.get_cb_file_for_comic(comic)
        extract_path = domain.get_extract_path_for_comic(comic)
        domain.get_comic_page_paths(cb_file=cb_file, extract_path=extract_path)
