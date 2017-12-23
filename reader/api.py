import base64
import json

from django.urls import reverse
from rarfile import RarFile
from zipfile import ZipFile

from django.http import HttpResponse

from reader.utils import (
    clear_tmp,
    extract_comic_page,
    get_comic_page_names,
    get_extracted_comic_page,
)


def comic_page(request, comic_path, page_number):
    try:
        decoded_comic_path = base64.decodebytes(bytes(comic_path, 'utf-8')).decode('utf-8')
        clear_tmp()

        # Create a zip or a rar file depending on the comic file type.
        if decoded_comic_path.endswith('.cbz'):
            cb_file = ZipFile(decoded_comic_path)
        else:
            cb_file = RarFile(decoded_comic_path)

        # Extract the page.
        extract_comic_page(cb_file=cb_file, page_number=page_number)

        # Calculate page numbers.
        previous_page_url = None
        next_page_url = None
        if page_number > 0:
            previous_page = page_number - 1
            previous_page_url = reverse('reader:comic_detail', kwargs={'comic_path': comic_path, 'page_number': previous_page})
        if page_number < len(get_comic_page_names(cb_file)) - 1:
            next_page = page_number + 1
            next_page_url = reverse('reader:comic_detail', kwargs={'comic_path': comic_path, 'page_number': next_page})

        return HttpResponse(json.dumps({
            'page_src': get_extracted_comic_page(),
            'previous_page': previous_page_url,
            'next_page': next_page_url,
        }), content_type='application/json')
    # TODO: A /favicon.ico request keeps causing KeyErrors, fix it.
    except KeyError as e:
        return HttpResponse('')
