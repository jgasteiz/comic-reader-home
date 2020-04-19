import json
import logging

from django.http import Http404, HttpResponse
from django.shortcuts import get_object_or_404
from django.views.decorators.csrf import csrf_exempt
from django.views.static import serve
from rest_framework import viewsets
from rest_framework.response import Response

from reader import models, serializers
from reader.domain import bookmarks, file_handler


class FileItemViewSet(viewsets.ModelViewSet):
    serializer_class = serializers.FileItemSerializer
    search_serializer_class = serializers.SimpleFileItemSerializer
    queryset = models.FileItem.objects.all()

    def list(self, request, **kwargs):
        if request.GET.get("q"):
            queryset = self.queryset.filter(name__icontains=request.GET.get("q"))
            serializer_class = self.search_serializer_class
        else:
            queryset = self.queryset.filter(parent=None)
            serializer_class = self.serializer_class
        serializer = serializer_class(queryset, context={"request": request}, many=True)
        return Response(serializer.data)

    def retrieve(self, request, pk=None, **kwargs):
        file_item = get_object_or_404(self.queryset, pk=pk)
        serializer = self.serializer_class(file_item, context={"request": request})
        return Response(serializer.data)


def comic_page_src(request, comic_id, page_number):
    try:
        comic = get_object_or_404(models.FileItem, pk=comic_id)
    except FileNotFoundError:
        return HttpResponse("Comic not found", status=404)
    try:
        page = file_handler.get_extracted_comic_page(comic, page_number)
        return serve(request, page, document_root="/")
    except Http404 as e:
        return HttpResponse("Page not found. Reason: {}".format(e), status=404)


# TODO: remove the `csrf_exempt` as soon as csrf is dealt with properly in the FE.
@csrf_exempt
def bookmark_comic_page(request):
    body_unicode = request.body.decode("utf-8")
    payload = json.loads(body_unicode)
    serializer = serializers.BookmarkSerializer(data=payload)
    if not serializer.is_valid():
        return Response(serializer.errors, status=400)

    try:
        comic_id = serializer.validated_data["comic_id"]
        page_number = serializer.validated_data["page_number"]
        comic = get_object_or_404(models.FileItem, pk=comic_id)
        bookmarks.bookmark_page(comic, page_number)
        return HttpResponse(
            json.dumps({"comic_id": comic_id, "page_number": page_number}),
            content_type="application/json",
        )
    except Exception as e:
        logging.critical(e)
        return HttpResponse({"error": e}, status=400)


@csrf_exempt
def delete_bookmark(request):
    body_unicode = request.body.decode("utf-8")
    payload = json.loads(body_unicode)
    comic = get_object_or_404(models.FileItem, pk=payload["comic_id"])
    bookmarks.delete_bookmark(comic)
    return HttpResponse("Bookmark deleted")
