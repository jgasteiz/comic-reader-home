from django import http, shortcuts
from django.views.static import serve

from reader import models
from reader.domain import file_handler


def directory(request, *args, **kwargs):
    queryset = models.FileItem.objects.all()
    if "fileitem_id" in kwargs:
        parent = queryset.get(id=kwargs["fileitem_id"])
    else:
        parent = queryset.get(parent__isnull=True)

    if request.GET.get("q"):
        directory_list = queryset.filter(
            file_type=models.FileItem.DIRECTORY, name__icontains=request.GET.get("q")
        )
        comic_list = queryset.filter(
            file_type=models.FileItem.COMIC, name__icontains=request.GET.get("q")
        )
    else:
        directory_list = queryset.filter(
            parent=parent, file_type=models.FileItem.DIRECTORY
        )
        comic_list = queryset.filter(parent=parent, file_type=models.FileItem.COMIC)

    return shortcuts.render(
        request,
        template_name="reader/home.html",
        context={
            "parent": parent,
            "directory_list": directory_list,
            "comic_list": comic_list,
        },
    )


def read_comic_page(request, comic_id, *args, **kwargs):
    page_number = int(request.GET.get("page_number", "0"))
    comic = shortcuts.get_object_or_404(models.FileItem, pk=comic_id)
    # Set the furthest read page
    comic.set_furthest_read_page(page_number)
    num_pages = comic.num_pages

    return shortcuts.render(
        request,
        template_name="reader/read.html",
        context={
            "comic_id": comic_id,
            "page_number": page_number,
            "previous_page_number": page_number - 1,
            "next_page_number": page_number + 1,
            "parent_id": comic.parent.id,
            "num_pages": num_pages,
            "num_pages_range": range(num_pages),
            "current_page_number": page_number,
        },
    )


def comic_page_src(request, comic_id, page_number):
    try:
        comic = shortcuts.get_object_or_404(models.FileItem, pk=comic_id)
    except FileNotFoundError:
        return http.HttpResponse("Comic not found", status=404)
    try:
        page = file_handler.get_extracted_comic_page(comic, page_number)
        return serve(request, page, document_root="/")
    except http.Http404 as e:
        return http.HttpResponse("Page not found. Reason: {}".format(e), status=404)
