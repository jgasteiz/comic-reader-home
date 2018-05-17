import logging
import os
from zipfile import ZipFile

from django.conf import settings
from django.http import Http404
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from rarfile import RarFile

from .models import FileItem


def get_encoded_path(decoded_path):
    return urlsafe_base64_encode(bytes(decoded_path, 'utf-8')).decode('utf-8').replace('\n', '')


def get_decoded_path(encoded_path):
    return urlsafe_base64_decode(bytes(encoded_path, 'utf-8')).decode('utf-8')


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


def get_extracted_comic_page(comic, page_number):
    """
    Extract the given page number or do nothing if it has been extracted already.
    """
    extract_path = get_extract_path_for_comic(comic)
    cb_file = get_cb_file_for_comic(comic)

    # Set all the page names in order
    comic_pages = sorted([
        p for p in cb_file.namelist()
        if p.endswith('.jpg') or p.endswith('.jpeg') or p.endswith('.png')
    ])

    try:
        page_file_name = comic_pages[page_number]
    except IndexError:
        raise Http404

    page_file_path = os.path.join(extract_path, page_file_name)

    # If it exists already, return it.
    if os.path.exists(page_file_path):
        logging.info('Page exists, no need to extract it.')
        return page_file_path

    # Need to make sure we create the extract path because
    # linux unrar-free won't create it if it doesn't exist.
    if not os.path.exists(extract_path):
        os.mkdir(extract_path)

    # Extract the actual page.
    cb_file.extract(page_file_name, extract_path)

    # And if it exists, return it.
    if os.path.exists(page_file_path):
        logging.info('Page extracted')
        return page_file_path

    # Otherwise something went wrong, raise 404.
    raise Http404


def extract_everything():
    """
    Extract every comic in the comic directory.
    """
    for comic in FileItem.objects.filter(file_type=FileItem.COMIC):
        extract_path = get_extract_path_for_comic(comic)
        cb_file = get_cb_file_for_comic(comic)
        if not os.path.exists(extract_path):
            os.mkdir(extract_path)
            cb_file.extractall(extract_path)
