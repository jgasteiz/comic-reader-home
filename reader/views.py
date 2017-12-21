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


def comic_detail(request, comic_path):
    try:
        comic_path = base64.decodebytes(bytes(comic_path, 'utf-8')).decode('utf-8')
        _clear_tmp()
        if comic_path.endswith('.cbz'):
            _extract_cbz_comic(comic_path=comic_path)
        else:
            _extract_cbr_comic(comic_path=comic_path)
        return render(
            request,
            template_name='reader/comic_detail.html',
            context={
                'comic_pages': _get_extracted_comic_pages()
            }
        )
    # TODO: A /favicon.ico request keeps causing KeyErrors, fix it.
    except KeyError as e:
        return HttpResponse('')


def _clear_tmp():
    """
    Clear the tmp directory.
    :return:
    """
    os.system('rm -rf {}/*'.format(settings.COMIC_TMP_PATH))


def _extract_cbz_comic(comic_path):
    """
    Extract the cbz file for the given comic path.
    :param comic_path:
    :return:
    """
    with ZipFile(comic_path) as cbz:
        for file in cbz.filelist:
            try:
                assert file.file_size > 1000
                assert file.filename.endswith('.jpg')
            except AssertionError:
                continue

            # Extract to tmp
            cbz.extract(file.filename, settings.COMIC_TMP_PATH)


def _extract_cbr_comic(comic_path):
    """
    Extract the cbr file for the given comic path.
    """
    cbr = RarFile(comic_path)
    cbr.extractall(path=settings.COMIC_TMP_PATH)


def _get_extracted_comic_pages():
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

    return sorted(comic_pages)


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
