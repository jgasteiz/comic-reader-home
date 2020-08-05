import pytest
from django import shortcuts

from reader import models

pytestmark = pytest.mark.django_db


def test_directory_root(client):
    root_directory = models.FileItem.objects.get(
        file_type=models.FileItem.DIRECTORY, parent__isnull=True
    )
    comic_directory = models.FileItem.objects.get(
        file_type=models.FileItem.DIRECTORY, parent=root_directory
    )

    url = shortcuts.reverse("reader:directory")
    response = client.get(url)

    assert response.status_code == 200
    assert response.context["parent"] == root_directory
    assert response.context["directory_list"].count() == 1
    assert response.context["directory_list"].first() == comic_directory
    assert response.context["comic_list"].count() == 0


def test_directory_detail(client):
    comic_directory = models.FileItem.objects.get(
        file_type=models.FileItem.DIRECTORY, parent__isnull=False
    )
    comic = models.FileItem.objects.get(
        file_type=models.FileItem.COMIC, parent=comic_directory
    )

    url = shortcuts.reverse(
        "reader:directory", kwargs={"fileitem_id": comic_directory.id}
    )
    response = client.get(url)

    assert response.status_code == 200
    assert response.context["parent"] == comic_directory
    assert response.context["directory_list"].count() == 0
    assert response.context["comic_list"].count() == 1
    assert response.context["comic_list"].first() == comic


def test_comic_detail(client):
    comic_directory = models.FileItem.objects.get(
        file_type=models.FileItem.DIRECTORY, parent__isnull=False
    )
    comic = models.FileItem.objects.get(
        file_type=models.FileItem.COMIC, parent=comic_directory
    )

    url = shortcuts.reverse("reader:read_comic_page", kwargs={"comic_id": comic.id})
    response = client.get(url)

    assert response.status_code == 200
    assert response.context["comic_id"] == comic.id
    assert response.context["previous_page_number"] == -1
    assert response.context["next_page_number"] == 1
    assert response.context["parent_id"] == comic_directory.id
    assert response.context["num_pages"] == 3
    assert response.context["current_page_number"] == 0
    assert response.context["current_page_width"] == 100
