import base64
import os
import subprocess

from django.http import HttpResponse
from rarfile import RarFile
from zipfile import ZipFile

from django.conf import settings
from django.shortcuts import render
from django.urls import reverse


def global_index(request):
    return render(
        request,
        template_name='reader/global_index.html',
        context={
            'comic_sections': [
                ('dark-horse-comics', 'Dark Horse Comics'),
                ('european', 'European comic'),
                ('marvel', 'Marvel Comics'),
            ],
        }
    )


def comic_index(request, comic_section):
    try:
        section_path = settings.COMICS_ROOT[comic_section]
        tree_html = _get_html_for_path(_get_path_contents(section_path, 'root'))
        return render(
            request,
            template_name='reader/comic_index.html',
            context={
                'tree_html': tree_html,
            }
        )
    except AttributeError as e:
        return HttpResponse('')


def comic_detail(request, comic_path):
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

    This requires `unrar` to be installed: `brew install unrar`.
    :param comic_path:
    :return:
    """
    cbr = RarFile(comic_path)
    cbr.extractall(path=settings.COMIC_TMP_PATH)


def _get_extracted_comic_pages():
    """
    Get the urls of the extracted comic pages.
    :return:
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
    - get the children paths in that path and their data.

    :param path: object
    :param path_name: str
    :return: object
    :rtype: object
    """
    # The the path comic files
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

        path_info['children'].append(
            _get_path_contents(path=child_path, path_name=path_name)
        )

    # Sort the comic names and child path names by name.
    path_info['comics'] = sorted(path_info['comics'], key=lambda x: x['name'])
    path_info['children'] = sorted(path_info['children'], key=lambda x: x['name'])

    return path_info


def _get_html_for_path(path):
    """
    Return an <ul> item with an <li> per comic or child path in the given path.
    :param path: object
    :return: string
    """
    html = ''

    if len(path['comics']) > 0:
        html += '<ul>'
        for comic in path['comics']:
            html += '<li><a target="_blank" href="{comic_detail_url}">{comic_name}</a></li>'.format(
                comic_detail_url=reverse('reader:comic_detail', kwargs={'comic_path': comic['path']}),
                comic_name=comic['name']
            )
        html += '</ul>'

    if len(path['children']) > 0:
        html += '<ul>'
        for child_path in path['children']:
            html += '<li><strong>{}</strong>'.format(child_path['name'])
            html += _get_html_for_path(child_path)
            html += '</li>'
        html += '</ul>'

    return html
