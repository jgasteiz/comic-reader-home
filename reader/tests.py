import os
from unittest import TestCase

from django.conf import settings
from django.test import Client
from django.urls import reverse

from reader.utils import get_encoded_path


class ApiTests(TestCase):

    def setUp(self):
        super(ApiTests, self).setUp()
        self.client = Client()

    def test_root_directory(self):
        url = reverse('reader:api_directory_root')
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)

        response_json = response.json()
        self.assertEqual(response_json.get('directory_path'), None)
        self.assertEqual(response_json.get('is_root'), True)

        path_contents = response_json.get('path_contents')
        self.assertEqual(path_contents.get('comics'), [])
        self.assertEqual(path_contents.get('name'), 'comics')
        directories = path_contents.get('directories')
        self.assertEqual(len(directories), 1)
        self.assertEqual(directories[0].get('name'), 'Javi Comics')
        self.assertTrue('path' in directories[0].keys())

    def test_image_comics_directory(self):
        image_comics_path = os.path.join(settings.COMICS_ROOT, 'Javi Comics')
        directory_path = get_encoded_path(image_comics_path)

        url = reverse('reader:api_directory', kwargs={'directory_path': directory_path})
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)

        response_json = response.json()
        self.assertEqual(response_json.get('directory_path'), directory_path)
        self.assertEqual(response_json.get('is_root'), False)

        path_contents = response_json.get('path_contents')
        self.assertEqual(path_contents.get('directories'), [])
        self.assertEqual(path_contents.get('name'), 'Javi Comics')
        comics = path_contents.get('comics')
        self.assertEqual(len(comics), 1)
        self.assertEqual(comics[0].get('name'), '01 - A Comic.cbz')
        self.assertTrue('path' in comics[0].keys())

    def test_comic_detail(self):
        image_comics_path = os.path.join(settings.COMICS_ROOT, 'Javi Comics')
        directory_path = get_encoded_path(image_comics_path)

        # Get the path of the comic.
        url = reverse('reader:api_directory', kwargs={'directory_path': directory_path})
        response = self.client.get(url)
        response_json = response.json()
        path_contents = response_json.get('path_contents')
        comic = path_contents.get('comics')[0]

        # Get the comic details
        url = reverse('reader:api_comic_detail', kwargs={'comic_path': comic.get('path')})
        response = self.client.get(url)
        response_json = response.json()
        self.assertEqual(response_json.get('comic_name'), '01 - A Comic.cbz')
        self.assertTrue(response_json.get('num_pages') > 2)
