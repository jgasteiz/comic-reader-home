import json
import logging

from django.http import HttpResponse, Http404
from django.views.decorators.csrf import csrf_exempt
from django.views.static import serve

from reader.utils import Comic, Directory


def directory_view(_, directory_path=None):
    try:
        directory = Directory(directory_path)
    except FileNotFoundError:
        return HttpResponse('Directory not found', status=404)

    directory_details = directory.get_details(include_bookmarks=False)
    return HttpResponse(json.dumps(directory_details), content_type='application/json')


def comic_detail(_, comic_path):
    try:
        comic = Comic(comic_path)
    except FileNotFoundError:
        return HttpResponse('Comic not found', status=404)

    return HttpResponse(json.dumps({
        'comic_name': comic.name,
        'num_pages': len(comic),
    }), content_type='application/json')


def comic_page_src(request, comic_path, page_number):
    try:
        comic = Comic(comic_path)
    except FileNotFoundError:
        return HttpResponse('Comic not found', status=404)
    try:
        return serve(request, comic.get_extracted_comic_page(page_number), document_root='/')
    except Http404 as e:
        return HttpResponse('Page not found. Reason: {}'.format(e), status=404)


# TODO: remove the `csrf_exempt` as soon as csrf is dealt with properly in the FE.
@csrf_exempt
def bookmark_comic_page(request):
    try:
        body_unicode = request.body.decode('utf-8')
        payload = json.loads(body_unicode)
        comic_path = payload.get('comic_path')
        page_number = payload.get('page_num')
        comic = Comic(comic_path)
        comic.bookmark_page(page_number)
        return HttpResponse(
            json.dumps({'comic_path': comic.path, 'page_num': page_number}),
            content_type='application/json',
        )
    except Exception as e:
        logging.critical(e)
        return HttpResponse(
            json.dumps({'error': e}),
            content_type='application/json',
            status=400,
        )
