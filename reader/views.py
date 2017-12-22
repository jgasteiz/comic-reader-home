import base64
import os

from rarfile import RarFile
from zipfile import ZipFile

from django.conf import settings
from django.http import HttpResponse
from django.shortcuts import render


def directory_detail(request, directory_path=None):
    try:
        if directory_path:
            directory_path = base64.decodebytes(bytes(directory_path, 'utf-8')).decode('utf-8')
        else:
            directory_path = settings.COMICS_ROOT
        directory_name = directory_path.split('/')[-1]
        path_contents = _get_path_contents(directory_path, directory_name)
        return render(
            request,
            template_name='reader/directory_detail.html',
            context={
                'path_contents': path_contents
            }
        )
    # TODO: A /favicon.ico request keeps causing KeyErrors, fix it.
    except KeyError as e:
        return HttpResponse('')


def comic_detail(request, comic_path, page_number=1):
    try:
        decoded_comic_path = base64.decodebytes(bytes(comic_path, 'utf-8')).decode('utf-8')
        _clear_tmp()

        # Create a zip or a rar file depending on the comic file type.
        if decoded_comic_path.endswith('.cbz'):
            cb_file = ZipFile(decoded_comic_path)
        else:
            cb_file = RarFile(decoded_comic_path)

        # Extract the page.
        _extract_comic_page(cb_file=cb_file, page_number=page_number)

        # Calculate page numbers.
        previous_page = None
        next_page = None
        if page_number > 0:
            previous_page = page_number - 1
        if page_number < len(_get_comic_page_names(cb_file)) - 1:
            next_page = page_number + 1

        return render(
            request,
            template_name='reader/comic_detail.html',
            context={
                'comic_page': _get_extracted_comic_page(),
                'previous_page': previous_page,
                'next_page': next_page,
                'comic_path': comic_path,
            }
        )
    # TODO: A /favicon.ico request keeps causing KeyErrors, fix it.
    except KeyError as e:
        return HttpResponse('')


def _clear_tmp():
    """
    Clear the tmp directory.
    """
    os.system('rm -rf {}/*'.format(settings.COMIC_TMP_PATH))


def _extract_comic_page(cb_file, page_number):
    """
    Extract the given page for the given comic file.
    """
    cb_file.extract(_get_comic_page_names(cb_file)[page_number], settings.COMIC_TMP_PATH)


def _get_comic_page_names(cb_file):
    """
    Get the given cb_file filenames which are .jpg or .png.
    """
    page_names = sorted(cb_file.namelist())
    return [p for p in page_names if p.endswith('.jpg') or p.endswith('.png')]


def _get_extracted_comic_page():
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


def _get_path_contents(path, path_name):
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
