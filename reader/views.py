import base64

from django.conf import settings
from django.http import HttpResponse
from django.shortcuts import render

from reader.utils import get_path_contents
from reader.tasks import extract_comic_file


def directory_detail(request, directory_path=None):
    try:
        if directory_path:
            directory_path = base64.decodebytes(bytes(directory_path, 'utf-8')).decode('utf-8')
        else:
            directory_path = settings.COMICS_ROOT
        directory_name = directory_path.split('/')[-1]
        path_contents = get_path_contents(directory_path, directory_name)
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


def comic_detail(request, comic_path, page_number):
    _comic_path = base64.decodebytes(bytes(comic_path, 'utf-8')).decode('utf-8')
    # Extract the entire comic file on a task
    extract_comic_file.delay(_comic_path, settings.COMIC_TMP_PATH)
    return render(
        request,
        template_name='reader/comic_detail.html',
        context={
            'comic_path': comic_path,
            'page_number': page_number,
            'comic_name': _comic_path.split('/')[-1],
        }
    )
