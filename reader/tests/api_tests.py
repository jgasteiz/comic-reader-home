import json
import os

import pytest
from django.conf import settings
from django.http import FileResponse
from django.test import Client
from django.urls import reverse

from reader.models import Bookmark
from reader.utils import Utils, Directory, Comic


def test_api_directory_root():
    client = Client()
    directory = Directory(path=None)

    # Get the path of the root directory, check the directory properties.
    url = reverse('reader:api_directory_root')
    response = client.get(url)
    response_json = response.json()
    assert response.status_code == 200
    assert sorted(response_json.keys()) == ['directory_path', 'is_root', 'parent_path', 'path_contents']
    assert response_json.get('directory_path') is None
    assert response_json.get('is_root') is True
    assert response_json.get('parent_path') == directory.parent_path

    # Check the path contents.
    path_contents = response_json.get('path_contents')
    assert sorted(path_contents.keys()) == ['comics', 'directories', 'name']
    assert path_contents.get('comics') == []
    directories = path_contents.get('directories')
    assert len(directories) == 1
    assert directories[0].get('name') == 'Javi Comics'
    assert 'path' in directories[0].keys()
    assert path_contents.get('name') == 'comics'


def test_api_directory():
    client = Client()

    image_comics_path = os.path.join(settings.COMICS_ROOT, 'Javi Comics')
    directory = Directory(path=Utils().get_encoded_path(image_comics_path))

    # Get the path of the directory, check the directory properties.
    url = reverse('reader:api_directory', kwargs={'directory_path': directory.path})
    response = client.get(url)
    response_json = response.json()
    assert response.status_code == 200
    assert sorted(response_json.keys()) == ['directory_path', 'is_root', 'parent_path', 'path_contents']
    assert response_json.get('directory_path') == directory.path
    assert response_json.get('is_root') is False
    assert response_json.get('parent_path') == directory.parent_path

    # Check the path contents.
    path_contents = response_json.get('path_contents')
    assert sorted(path_contents.keys()) == ['comics', 'directories', 'name']
    comics = path_contents.get('comics')
    assert len(comics) == 1
    assert comics[0].get('name') == '01 - A Comic.cbz'
    assert 'path' in comics[0].keys()
    assert path_contents.get('directories') == []
    assert path_contents.get('name') == 'Javi Comics'


def test_api_comic_detail():
    client = Client()

    image_comics_path = os.path.join(settings.COMICS_ROOT, 'Javi Comics')
    directory = Directory(path=Utils().get_encoded_path(image_comics_path))

    # Get the path of the comic and create a comic instance.
    url = reverse('reader:api_directory', kwargs={'directory_path': directory.path})
    response = client.get(url)
    comic_json = response.json().get('path_contents').get('comics')[0]
    comic = Comic(path=comic_json.get('path'))

    # Check the comic details.
    url = reverse('reader:api_comic_detail', kwargs={'comic_path': comic.path})
    response = client.get(url)
    response_json = response.json()
    assert response_json.get('comic_name') == comic.name
    assert response_json.get('num_pages') == 3
    assert response_json.get('parent_path') == comic.get_parent_path()


# TODO: CircleCI won't run `os.mkdir`, look into it and fix it.
@pytest.mark.skip
def test_api_comic_page_src():
    client = Client()

    image_comics_path = os.path.join(settings.COMICS_ROOT, 'Javi Comics')
    directory = Directory(path=Utils().get_encoded_path(image_comics_path))

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


@pytest.mark.django_db
def test_bookmark_comic_page():
    client = Client()

    image_comics_path = os.path.join(settings.COMICS_ROOT, 'Javi Comics')
    directory = Directory(path=Utils().get_encoded_path(image_comics_path))

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
