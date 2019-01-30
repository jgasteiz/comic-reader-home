import logging
import os
from zipfile import ZipFile

from django.conf import settings
from django.http import Http404
from rarfile import RarFile

from reader import models


def clear_tmp():
    """
    Clear the tmp directory.
    """
    os.system('rm -rf {}/*'.format(settings.COMIC_EXTRACT_PATH))


def is_file_name_comic_file(file_name):
    """
    Checks whether a given file name is a valid comic file name or not.
    """
    if not file_name.endswith('.cbz') and not file_name.endswith('.cbr'):
        return False
    if file_name.startswith('.'):
        return False
    return True


def get_cb_file_for_comic(comic):
    """
    Initialise the cb_file. This will raise a FileNotFoundError if
    zipfile/rarfile can't find the file.
    """
    if comic.path.endswith('.cbz'):
        return ZipFile(comic.path)
    return RarFile(comic.path)


def get_extract_path_for_comic(comic):
    return os.path.join(settings.COMIC_EXTRACT_PATH, str(comic.pk))


def get_extracted_comic_pages(comic, page_numbers):
    """
    Extract the given page numbers.
    """
    extract_path = get_extract_path_for_comic(comic)
    cb_file = get_cb_file_for_comic(comic)

    # Set all the page names in order
    comic_pages = sorted([
        p for p in cb_file.namelist()
        if p.endswith('.jpg') or p.endswith('.jpeg') or p.endswith('.png')
    ])

    page_file_paths = []
    for page_number in page_numbers:
        try:
            page_file_name = comic_pages[page_number]
        except IndexError:
            raise Http404

        page_file_path = os.path.join(extract_path, page_file_name)

        # If it exists already, return it.
        if os.path.exists(page_file_path):
            logging.info('Page exists, no need to extract it.')
            page_file_paths.append(page_file_path)
            continue

        # Need to make sure we create the extract path because
        # linux unrar-free won't create it if it doesn't exist.
        if not os.path.exists(extract_path):
            os.mkdir(extract_path)

        # Extract the actual page.
        cb_file.extract(page_file_name, extract_path)

        # And if it exists, return it.
        if os.path.exists(page_file_path):
            logging.info('Page extracted')
            page_file_paths.append(page_file_path)

    if len(page_file_paths) == 0:
        raise Http404

    return page_file_paths


def get_extracted_comic_page(comic, page_number):
    """
    Extract the given page number or do nothing if it has been extracted already.
    """
    return get_extracted_comic_pages(comic, [page_number])[0]


def extract_everything():
    """
    Extract every comic in the comic directory.
    """
    for comic in models.FileItem.objects.filter(file_type=models.FileItem.COMIC):
        extract_path = get_extract_path_for_comic(comic)
        cb_file = get_cb_file_for_comic(comic)
        if not os.path.exists(extract_path):
            os.mkdir(extract_path)
            cb_file.extractall(extract_path)


def get_or_create_file_item(path, parent):
    """
    Create or retrieve an existing file for a given path and parent.
    """
    file_item, _ = models.FileItem.objects.get_or_create(path=path, parent=parent)
    file_item.set_name()
    file_item.set_file_type()
    return file_item
