import base64
import json

from rarfile import RarFile
from zipfile import ZipFile

from django.http import HttpResponse

from reader.utils import (
    get_extracted_comic_page,
    get_num_comic_pages
)


def comic_page(request, comic_path, page_number):
    try:
        decoded_comic_path = base64.decodebytes(bytes(comic_path, 'utf-8')).decode('utf-8')

        # Create a zip or a rar file depending on the comic file type.
        if decoded_comic_path.endswith('.cbz'):
            cb_file = ZipFile(decoded_comic_path)
        else:
            cb_file = RarFile(decoded_comic_path)

        # Calculate page numbers.
        has_previous_page = False
        has_next_page = False
        num_pages = get_num_comic_pages(cb_file)
        if page_number > 0:
            has_previous_page = True
        if page_number < num_pages - 1:
            has_next_page = True

        return HttpResponse(json.dumps({
            'page_src': get_extracted_comic_page(cb_file=cb_file, page_number=page_number, comic_path=decoded_comic_path),
            'has_previous_page': has_previous_page,
            'has_next_page': has_next_page,
            'num_pages': num_pages
        }), content_type='application/json')
    # TODO: A /favicon.ico request keeps causing KeyErrors, fix it.
    except KeyError as e:
        return HttpResponse('')
