import base64
import os
from zipfile import (
    ZipFile,
)

from django.conf import settings
from django.shortcuts import render


def comic_index(request):
    comic_list = os.listdir(settings.COMICS_ROOT)
    comic_list = [(f, base64.encodebytes(bytes(f, 'utf-8')).decode('utf-8'))
                  for f in comic_list
                  if f.endswith('.cbz')]
    return render(
        request,
        template_name='reader/comic_index.html',
        context={
            'comic_list': comic_list
        }
    )


def comic_detail(request, file_name):
    file_name = base64.decodebytes(bytes(file_name, 'utf-8')).decode('utf-8')
    _clear_tmp()
    _extract_comic(comic_path=os.path.join(settings.COMICS_ROOT, file_name))
    return render(
        request,
        template_name='reader/comic_detail.html',
        context={
            'comic_pages': _get_extracted_comic_pages()
        }
    )


def _clear_tmp():
    """
    Clear the tmp directory.
    :return:
    """
    os.system('rm -rf {}/*'.format(settings.COMIC_TMP_PATH))


def _extract_comic(comic_path):
    """
    Extract the comic for the given comic path.
    :param comic_path:
    :return:
    """
    with ZipFile(comic_path) as cbz:
        for file in cbz.filelist:
            try:
                assert file.file_size > 1000
                assert file.filename.endswith('.jpg')
            except AssertionError:
                continue

            # Extract to tmp
            cbz.extract(file.filename, settings.COMIC_TMP_PATH)


def _get_extracted_comic_pages():
    """
    Get the urls of the extracted comic pages.
    :return:
    """
    comic_pages = []
    for file_name in os.listdir(settings.COMIC_TMP_PATH):
        file_path = os.path.join(settings.COMIC_TMP_PATH, file_name)

        if file_name == '.DS_Store':
            continue

        if os.path.isdir(file_path):
            for file_name_2 in os.listdir(file_path):
                file_path_2 = os.path.join(file_path, file_name_2)
                comic_pages.append(file_path_2)
        else:
            comic_pages.append(file_path)

    # Remove the absolute path from the comic urls
    comic_pages = [p.replace(settings.BASE_DIR, '') for p in comic_pages]

    return sorted(comic_pages)
