import base64
import json
import logging

from django.urls import reverse
from django.views.decorators.csrf import csrf_exempt
from django.views.static import serve
from rarfile import RarFile
from zipfile import ZipFile

from django.http import HttpResponse

from reader.models import Bookmark
from reader.utils import (
    get_extracted_comic_page,
    get_num_comic_pages,
    get_directory_details,
)


def directory(request, directory_path=None):
    directory_details = get_directory_details(directory_path)
    return HttpResponse(json.dumps(directory_details), content_type='application/json')


def comic_detail(request, comic_path):
    decoded_comic_path = base64.decodebytes(bytes(comic_path, 'utf-8')).decode('utf-8')

    # Create a zip or a rar file depending on the comic file type.
    if decoded_comic_path.endswith('.cbz'):
        cb_file = ZipFile(decoded_comic_path)
    else:
        cb_file = RarFile(decoded_comic_path)
    return HttpResponse(json.dumps({

        'comic_name': decoded_comic_path.split('/')[-1],
        'num_pages': get_num_comic_pages(cb_file),
    }), content_type='application/json')


def comic_page_src(request, comic_path, page_number):
    decoded_comic_path = base64.decodebytes(bytes(comic_path, 'utf-8')).decode('utf-8')

    # Create a zip or a rar file depending on the comic file type.
    if decoded_comic_path.endswith('.cbz'):
        cb_file = ZipFile(decoded_comic_path)
    else:
        cb_file = RarFile(decoded_comic_path)

    file_src = get_extracted_comic_page(cb_file=cb_file, page_number=page_number, comic_path=decoded_comic_path)

    return serve(request, file_src, document_root='')


# TODO: remove the `csrf_exempt` as soon as csrf is dealt with properly in the FE.
@csrf_exempt
def bookmark_comic_page(request):
    try:
        body_unicode = request.body.decode('utf-8')
        payload = json.loads(body_unicode)
        comic_path = payload.get('comic_path')
        decoded_comic_path = base64.decodebytes(bytes(comic_path, 'utf-8')).decode('utf-8')
        comic_path_components = decoded_comic_path.split('/')
        page_num = payload.get('page_num')
        bookmark, created = Bookmark.objects.get_or_create(
            comic_path=comic_path,
            title=comic_path_components[-1]
        )
        bookmark.page_num = page_num
        bookmark.save()
        return HttpResponse(
            json.dumps({'comic_path': comic_path, 'page_num': page_num}),
            content_type='application/json',
        )
    except Exception as e:
        logging.critical(e)
        return HttpResponse(
            json.dumps({'error': e}),
            content_type='application/json',
            status=400,
        )
