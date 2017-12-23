import base64
import os

from rarfile import RarFile
from zipfile import ZipFile

from django.conf import settings


def clear_tmp():
    """
    Clear the tmp directory.
    """
    os.system('rm -rf {}/*'.format(settings.COMIC_TMP_PATH))


def extract_comic_page(cb_file, page_number):
    """
    Extract the given page for the given comic file.
    """
    cb_file.extract(get_comic_page_names(cb_file)[page_number], settings.COMIC_TMP_PATH)


def get_comic_page_names(cb_file):
    """
    Get the given cb_file filenames which are .jpg or .png.
    """
    page_names = sorted(cb_file.namelist())
    return [p for p in page_names if p.endswith('.jpg') or p.endswith('.png')]


def get_extracted_comic_page():
    """
    Get the urls of the extracted comic pages.
    """
    comic_pages = []
    for file_name in os.listdir(settings.COMIC_TMP_PATH):
        file_path = os.path.join(settings.COMIC_TMP_PATH, file_name)

        if file_name in settings.IGNORED_FILE_NAMES:
            continue

        if os.path.isdir(file_path):
            for file_name_2 in os.listdir(file_path):
                file_path_2 = os.path.join(file_path, file_name_2)
                comic_pages.append(file_path_2)
        else:
            comic_pages.append(file_path)

    # Remove the absolute path from the comic urls
    comic_pages = [p.replace(settings.BASE_DIR, '') for p in comic_pages]

    return comic_pages[0]


def get_path_contents(path, path_name):
    """
    For a given path and path name:
    - get the comic files in that path
    - get the children directory paths in that path.
    """
    # Get the path comic files
    path_comics = []
    for comic_file_name in os.listdir(path):
        if not comic_file_name.endswith('.cbz') and not comic_file_name.endswith('.cbr'):
            continue
        if comic_file_name.startswith('.'):
            continue
        comic_file_path = os.path.join(path, comic_file_name)
        path_comics.append({
            'name': comic_file_name,
            'path': base64.encodebytes(bytes(comic_file_path, 'utf-8')).decode('utf-8'),
        })

    # Build the path info object
    path_info = {
        'name': path_name,
        'comics': path_comics,
        'children': []
    }
    # Per directory in the current path, get their path info.
    for path_name in os.listdir(path):
        child_path = os.path.join(path, path_name)

        # Ignore it if the child name is in IGNORED FILE NAMES or if it's
        # not a directory.
        if any([
            path_name in settings.IGNORED_FILE_NAMES,
            not os.path.isdir(child_path)
        ]):
            continue

        path_info['children'].append({
            'name': path_name,
            'path': base64.encodebytes(bytes(child_path, 'utf-8')).decode('utf-8'),
        })

    # Sort the comic names and child path names by name.
    path_info['comics'] = sorted(path_info['comics'], key=lambda x: x['name'])
    path_info['children'] = sorted(path_info['children'], key=lambda x: x['name'])

    return path_info
