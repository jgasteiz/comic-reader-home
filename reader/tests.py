from unittest import TestCase

from django.test import Client
from django.urls import reverse


class ApiTests(TestCase):

    def setUp(self):
        super(ApiTests, self).setUp()
        self.client = Client()

    def test_root_directory(self):
        response = self.client.get(reverse('reader:api_directory_root'))
        self.assertEqual(response.status_code, 200)

        response_json = response.json()
        self.assertEqual(response_json.get('directory_path'), None)
        self.assertEqual(response_json.get('is_root'), True)

        path_contents = response_json.get('path_contents')
        self.assertEqual(path_contents.get('comics'), [])
        self.assertEqual(path_contents.get('name'), 'comics')
        directories = path_contents.get('directories')
        self.assertEqual(len(directories), 1)
        self.assertEqual(directories[0].get('name'), 'Image Comics')
        self.assertTrue('path' in directories[0].keys())
