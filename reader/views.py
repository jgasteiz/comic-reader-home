import json

from django import http, shortcuts
from django.views.decorators.csrf import csrf_exempt
from django.views.static import serve

from reader import domain, models
from reader.application import read


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
        template_name="reader/directory.html",
        context={
            "parent": parent,
            "file_item_list": file_item_list,
        },
    )


def in_progress(request):
    comics = models.FileItem.objects.in_progress().order_by("name")
    return shortcuts.render(
        request,
        template_name="reader/in_progress.html",
        context={"comics": comics},
    )


def page(request, comic_id, *args, **kwargs):
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


def mark_comic_as_read(request, comic_id):
    if request.POST:
        comic = shortcuts.get_object_or_404(models.FileItem, pk=comic_id)
        domain.mark_comic_as_read(comic)
    return shortcuts.redirect(request.GET.get("next"))


def mark_comic_as_unread(request, comic_id):
    if request.POST:
        comic = shortcuts.get_object_or_404(models.FileItem, pk=comic_id)
        domain.mark_comic_as_unread(comic)
    return shortcuts.redirect(request.GET.get("next"))


def mark_directory_as_read(request, directory_id):
    if request.POST:
        comic_directory = shortcuts.get_object_or_404(models.FileItem, pk=directory_id)
        domain.mark_directory_as_read(comic_directory)
    return shortcuts.redirect(request.GET.get("next"))


def page_spa(request, comic_id):
    page_number = int(request.GET.get("page_number", "0"))
    comic = shortcuts.get_object_or_404(models.FileItem, pk=comic_id)

    num_pages = domain.get_num_pages(comic)
    domain.update_comic_status(comic, page_number)

    next_comic = domain.get_next_comic_in_directory(comic)
    next_comic_data = None
    if next_comic is not None:
        next_comic_data = {
            "name": next_comic.name,
            "url": shortcuts.reverse(
                "reader:read_comic_spa", kwargs={"comic_id": next_comic.id}
            )
            + "?page_number=0",
        }

    comic_data = {
        "comicId": comic_id,
        "numPages": num_pages,
        "initialPage": page_number,
        "parentDirectoryUrl": shortcuts.reverse(
            "reader:directory", kwargs={"fileitem_id": comic.parent.id}
        ),
        "pageSrcBaseUrl": f"/comic/{comic_id}/page/",
        "progressUrl": f"/comic/{comic_id}/progress/",
        "nextComic": next_comic_data,
    }

    return shortcuts.render(
        request,
        template_name="reader/read_spa.html",
        context={"comic_data_json": json.dumps(comic_data), "comic_name": comic.name},
    )


@csrf_exempt
def update_comic_progress(request, comic_id):
    if request.method != "POST":
        return http.JsonResponse({"error": "POST required"}, status=405)

    comic = shortcuts.get_object_or_404(models.FileItem, pk=comic_id)
    data = json.loads(request.body)
    page_number = data["page_number"]
    domain.update_comic_status(comic, page_number)
    return http.JsonResponse({"status": "ok"})


def page_src(request, comic_id, page_number):
    comic = shortcuts.get_object_or_404(models.FileItem, pk=comic_id)
    try:
        return serve(
            request=request,
            path=read.get_page_path(comic=comic, page_number=page_number),
            document_root="/",
        )
    except domain.UnableToExtractPage as e:
        return http.HttpResponse("Page not found. Reason: {}".format(e), status=404)
