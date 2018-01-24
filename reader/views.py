import base64

from django.conf import settings
from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.urls import reverse

from reader.models import Bookmark, Favorite
from reader.utils import get_path_contents
from reader.tasks import extract_comic_file


def directory_detail(request, directory_path=None):
    try:
        if directory_path:
            decoded_directory_path = base64.decodebytes(bytes(directory_path, 'utf-8')).decode('utf-8')
        else:
            decoded_directory_path = settings.COMICS_ROOT

        directory_name = decoded_directory_path.split('/')[-1]
        path_contents = get_path_contents(decoded_directory_path, directory_name)
        return render(
            request,
            template_name='reader/directory_detail.html',
            context={
                'path_contents': path_contents,
                'is_root': decoded_directory_path == settings.COMICS_ROOT,
                'directory_path': directory_path,
                'favorite_list': Favorite.objects.all()
            }
        )
    # TODO: A /favicon.ico request keeps causing KeyErrors, fix it.
    except KeyError as e:
        return HttpResponse('')


def comic_detail(request, comic_path, page_number):
    _comic_path = base64.decodebytes(bytes(comic_path, 'utf-8')).decode('utf-8')
    parent_path = _comic_path.split('/')[:-1]
    parent_path = '/'.join(parent_path)
    parent_path = base64.encodebytes(bytes(parent_path, 'utf-8')).decode('utf-8')
    parent_page_url = reverse('reader:directory_detail', kwargs={'directory_path': parent_path})
    # Extract the entire comic file on a task
    extract_comic_file.delay(_comic_path, settings.COMIC_TMP_PATH)
    return render(
        request,
        template_name='reader/comic_detail.html',
        context={
            'comic_path': comic_path,
            'parent_path': parent_page_url,
            'page_number': page_number,
            'comic_name': _comic_path.split('/')[-1],
        }
    )
