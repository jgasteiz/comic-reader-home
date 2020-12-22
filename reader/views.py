from django import http, shortcuts
from django.views.static import serve

from reader import domain, models


def directory(request, *args, **kwargs):
    queryset = models.FileItem.objects.all()
    if "fileitem_id" in kwargs:
        parent = queryset.get(id=kwargs["fileitem_id"])
    else:
        parent = queryset.get(parent__isnull=True)

    if request.GET.get("q"):
        file_item_list = queryset.filter(name__icontains=request.GET.get("q"))
    else:
        file_item_list = queryset.filter(parent=parent)

    return shortcuts.render(
        request,
        template_name="reader/home.html",
        context={
            "parent": parent,
            "file_item_list": file_item_list,
        },
    )


def read_comic_page(request, comic_id, *args, **kwargs):
    page_number = int(request.GET.get("page_number", "0"))
    page_width = int(request.GET.get("page_width", "100"))
    comic = shortcuts.get_object_or_404(models.FileItem, pk=comic_id)

    num_pages = domain.get_num_pages(comic)
    # Update the comic status: set furthest read page and whether is finished or not.
    domain.update_comic_status(comic, page_number)

    return shortcuts.render(
        request,
        template_name="reader/read.html",
        context={
            "comic_id": comic_id,
            "previous_page_number": page_number - 1,
            "next_page_number": page_number + 1,
            "parent_id": comic.parent.id,
            "num_pages": num_pages,
            "num_pages_range": range(num_pages),
            "current_page_number": page_number,
            "page_width_options": [100, 90, 80, 70, 60],
            "current_page_width": page_width,
        },
    )


def mark_as_unread(request, comic_id):
    if request.POST:
        comic = shortcuts.get_object_or_404(models.FileItem, pk=comic_id)
        print(f"Marking {comic} as unread")
        comic.mark_as_unread()
    return shortcuts.redirect(request.GET.get("next"))


def mark_as_read(request, comic_id):
    if request.POST:
        comic = shortcuts.get_object_or_404(models.FileItem, pk=comic_id)
        print(f"Marking {comic} as read")
        comic.mark_as_read()
    return shortcuts.redirect(request.GET.get("next"))


def mark_all_as_read(request, directory_id):
    if request.POST:
        comic_directory = shortcuts.get_object_or_404(models.FileItem, pk=directory_id)
        print(f"Marking all comics under directory {comic_directory} as read")
        domain.mark_directory_comics_as_read(comic_directory)
    return shortcuts.redirect(request.GET.get("next"))


def comic_page_src(request, comic_id, page_number):
    comic = shortcuts.get_object_or_404(models.FileItem, pk=comic_id)
    try:
        page = domain.get_comic_page_path(comic, page_number)
        return serve(request, page, document_root="/")
    except domain.UnableToExtractPage as e:
        return http.HttpResponse("Page not found. Reason: {}".format(e), status=404)
