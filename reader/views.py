import base64
from zipfile import ZipFile

from django.conf import settings
from django.shortcuts import render, redirect
from django.urls import reverse
from rarfile import RarFile

from reader.models import Bookmark, Favorite
from reader.utils import get_directory_details, get_num_comic_pages
from reader.tasks import extract_comic_file


def directory_detail(request, directory_path=None):
    directory_details = get_directory_details(directory_path)
    directory_details['favorite_list'] = Favorite.objects.all()
    return render(
        request,
        template_name='reader/directory_detail.html',
        context=directory_details
    )


def comic_detail(request, comic_path, page_number):
    decoded_comic_path = base64.decodebytes(bytes(comic_path, 'utf-8')).decode('utf-8')
    parent_path = decoded_comic_path.split('/')[:-1]
    parent_path = '/'.join(parent_path)
    parent_path = base64.encodebytes(bytes(parent_path, 'utf-8')).decode('utf-8')
    parent_page_url = reverse('reader:directory_detail', kwargs={'directory_path': parent_path})

    if settings.USE_CELERY:
        # Extract the entire comic file on a task
        extract_comic_file.delay(decoded_comic_path, settings.COMIC_TMP_PATH)

    if decoded_comic_path.endswith('.cbz'):
        cb_file = ZipFile(decoded_comic_path)
    else:
        cb_file = RarFile(decoded_comic_path)

    return render(
        request,
        template_name='reader/comic_detail.html',
        context={
            'comic_path': comic_path,
            'parent_path': parent_page_url,
            'page_number': page_number,
            'num_pages': get_num_comic_pages(cb_file),
            'comic_name': decoded_comic_path.split('/')[-1],
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
