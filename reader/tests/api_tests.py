import json
import os

import pytest
from django.conf import settings
from django.http import FileResponse
from django.test import Client
from django.urls import reverse

from reader.models import Bookmark, FileItem
from reader.serializers import FileItemSerializer, SimpleFileItemSerializer
from reader.tasks import populate_db_from_path
from reader.utils import Directory, Comic, get_encoded_path


# TODO: look how to do setup with pytest
def _setup():
    populate_db_from_path()


@pytest.mark.django_db
def test_api_directory_root():
    _setup()
    client = Client()

    root_dir = FileItem.objects.get(parent=None)
    root_dir_serialized = FileItemSerializer(root_dir).data
    javi_comics = FileItem.objects.get(parent=root_dir)
    javi_comics_serialized = SimpleFileItemSerializer(javi_comics).data

    # Get the path of the root directory, check the directory properties.
    url = reverse('reader:fileitem-list')
    response = client.get(url)
    response_json = response.json()
    assert response.status_code == 200
    # There should be only 1 item in the response list, the root directory.
    assert len(response_json) == 1
    root_dir_json = response_json[0]
    assert root_dir_json == root_dir_serialized

    # The root directory should have 1 child, `javi_comics`.
    assert len(root_dir_json.get('children')) == 1
    root_dir_child_json = root_dir_json.get('children')[0]
    assert root_dir_child_json == javi_comics_serialized


@pytest.mark.django_db
def test_api_directory():
    _setup()
    client = Client()

    root_dir = FileItem.objects.get(parent=None)
    javi_comics = FileItem.objects.get(parent=root_dir)
    javi_comics_serialized = FileItemSerializer(instance=javi_comics).data
    comic = FileItem.objects.get(parent=javi_comics)
    comic_serialized = SimpleFileItemSerializer(comic).data

    # Get the path of the root directory, check the directory properties.
    url = reverse('reader:fileitem-detail', kwargs={'pk': javi_comics.pk})
    response = client.get(url)
    response_json = response.json()
    assert response.status_code == 200
    # The response should be the javi_comics directory serialized.
    assert response_json == javi_comics_serialized

    # The root directory should have 1 child, "the comic cbz file".
    assert len(response_json.get('children')) == 1
    root_dir_child_json = response_json.get('children')[0]
    assert root_dir_child_json == comic_serialized


@pytest.mark.django_db
def test_api_comic_detail():
    _setup()
    client = Client()

    comic = FileItem.objects.get(file_type=FileItem.COMIC)
    comic_serialized = FileItemSerializer(comic).data

    # Get the path of the root directory, check the directory properties.
    url = reverse('reader:fileitem-detail', kwargs={'pk': comic.pk})
    response = client.get(url)
    response_json = response.json()
    assert response.status_code == 200
    # The response should be the test comic serialized, which should have 3 pages.
    assert response_json == comic_serialized


# TODO: CircleCI won't run `os.mkdir`, look into it and fix it.
@pytest.mark.skip
def test_api_comic_page_src():
    client = Client()

    image_comics_path = os.path.join(settings.COMICS_ROOT, 'Javi Comics')
    directory = Directory(path=get_encoded_path(image_comics_path))

    # Get the path of the comic and create a comic instance.
    url = reverse('reader:api_directory', kwargs={'directory_path': directory.path})
    response = client.get(url)
    comic_json = response.json().get('path_contents').get('comics')[0]
    comic = Comic(path=comic_json.get('path'))

    # Get a comic page.
    url = reverse('reader:api_comic_page_src', kwargs={'comic_path': comic.path, 'page_number': 2})
    response = client.get(url)
    assert response.status_code == 200
    assert type(response) == FileResponse
    # TODO: look into making sure we're returning the right page.


@pytest.mark.skip
@pytest.mark.django_db
def test_bookmark_comic_page():
    client = Client()

    image_comics_path = os.path.join(settings.COMICS_ROOT, 'Javi Comics')
    directory = Directory(path=get_encoded_path(image_comics_path))

    # Get the path of the comic and create a comic instance.
    url = reverse('reader:api_directory', kwargs={'directory_path': directory.path})
    response = client.get(url)
    comic_json = response.json().get('path_contents').get('comics')[0]
    comic = Comic(path=comic_json.get('path'))

    # Bookmark the page number 2.
    url = reverse('reader:bookmark_comic_page')
    payload = json.dumps({'comic_path': comic.path, 'page_num': 2})
    response = client.post(url, payload, content_type='application/json')
    response_json = response.json()
    assert response_json.get('comic_path') == comic.path
    assert response_json.get('page_num') == 2

    # A Bookmark should have been created.
    bookmark = Bookmark.objects.get()
    assert bookmark.title == comic.name
    assert bookmark.comic_path == comic.path
    assert bookmark.page_num == 2
