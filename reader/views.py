from django.conf import settings
from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.urls import reverse

from reader.models import Bookmark, Favorite
from reader.utils import Comic, Directory
from reader.tasks import extract_comic_file


def directory_detail(request, directory_path=None):
    try:
        directory = Directory(directory_path)
    except FileNotFoundError:
        return HttpResponse('Directory not found', status=404)

    ctx = directory.get_details(include_bookmarks=True)
    ctx['favorite_list'] = Favorite.objects.all()
    return render(
        request,
        template_name='reader/directory_detail.html',
        context=ctx,
    )


def comic_read(request, comic_path, page_number):
    """
    View that renders the comic reader.
    """
    comic = Comic(comic_path)

    if settings.USE_CELERY:
        # Extract the entire comic file on a task
        extract_comic_file.delay(comic_path)

    return render(
        request,
        template_name='reader/comic_read.html',
        context={
            'comic_path': comic.path,
            'parent_path': comic.get_parent_path_url(),
            'page_number': page_number,
            'num_pages': len(comic),
            'comic_name': comic.name,
        }
    )


def delete_bookmark(request):
    bookmark_id = request.POST.get('bookmark_id')
    directory_path = request.POST.get('next')

    if not bookmark_id or not directory_path:
        return redirect(reverse('reader:global_index'))

    try:
        Bookmark.objects.get(id=bookmark_id).delete()
        return redirect(reverse('reader:directory_detail', kwargs={'directory_path': directory_path}))
    except Bookmark.DoesNotExist as e:
        return redirect(reverse('reader:directory_detail', kwargs={'directory_path': directory_path}))
