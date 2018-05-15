import json
import logging

from django.http import HttpResponse, Http404
from django.shortcuts import get_object_or_404
from django.views.decorators.csrf import csrf_exempt
from django.views.static import serve
from rest_framework import viewsets
from rest_framework.response import Response

from ..models import FileItem
from ..serializers import FileItemSerializer
from ..utils import Comic


class FileItemViewSet(viewsets.ModelViewSet):
    serializer_class = FileItemSerializer
    queryset = FileItem.objects.all()

    def list(self, request, **kwargs):
        queryset = self.queryset.filter(parent=None)
        serializer = self.serializer_class(queryset, context={'request': request}, many=True)
        return Response(serializer.data)

    def retrieve(self, request, pk=None, **kwargs):
        file_item = get_object_or_404(self.queryset, pk=pk)
        serializer = self.serializer_class(file_item, context={'request': request})
        return Response(serializer.data)


def comic_page_src(request, comic_id, page_number):
    try:
        comic = Comic(comic_id)
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
