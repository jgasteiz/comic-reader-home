import os

from django.conf import settings
from django.test import Client
from django.urls import reverse

from reader.utils import Utils


def test_root_directory():
    client = Client()

    url = reverse('reader:api_directory_root')
    response = client.get(url)
    assert response.status_code == 200

    response_json = response.json()
    assert response_json.get('directory_path') is None
    assert response_json.get('is_root') == True

    path_contents = response_json.get('path_contents')
    assert path_contents.get('comics') == []
    assert path_contents.get('name') == 'comics'
    directories = path_contents.get('directories')
    assert len(directories) == 1
    assert directories[0].get('name') == 'Javi Comics'
    assert 'path' in directories[0].keys()


def test_javi_comics_directory():
    client = Client()

    image_comics_path = os.path.join(settings.COMICS_ROOT, 'Javi Comics')
    directory_path = Utils().get_encoded_path(image_comics_path)

    url = reverse('reader:api_directory', kwargs={'directory_path': directory_path})
    response = client.get(url)
    assert response.status_code == 200

    response_json = response.json()
    assert response_json.get('directory_path') == directory_path
    assert response_json.get('is_root') is False

    path_contents = response_json.get('path_contents')
    assert path_contents.get('directories') == []
    assert path_contents.get('name') == 'Javi Comics'
    comics = path_contents.get('comics')
    assert len(comics) == 1
    assert comics[0].get('name') == '01 - A Comic.cbz'
    assert 'path' in comics[0].keys()


def test_comic_detail():
    client = Client()

    image_comics_path = os.path.join(settings.COMICS_ROOT, 'Javi Comics')
    directory_path = Utils().get_encoded_path(image_comics_path)

    # Get the path of the comic.
    url = reverse('reader:api_directory', kwargs={'directory_path': directory_path})
    response = client.get(url)
    response_json = response.json()
    path_contents = response_json.get('path_contents')
    comic = path_contents.get('comics')[0]

    # Get the comic details
    url = reverse('reader:api_comic_detail', kwargs={'comic_path': comic.get('path')})
    response = client.get(url)
    response_json = response.json()
    assert response_json.get('comic_name') == '01 - A Comic.cbz'
    assert response_json.get('num_pages') > 2
