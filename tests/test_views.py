import datetime
import json

import pytest
from django import shortcuts
from django.utils import timezone

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
    assert response.context["file_item_list"].count() == 1
    assert response.context["file_item_list"].first() == comic_directory


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
    assert response.context["file_item_list"].count() == 1
    assert response.context["file_item_list"].first() == comic


def test_comic_detail(client):
    comic_directory = models.FileItem.objects.get(
        file_type=models.FileItem.DIRECTORY, parent__isnull=False
    )
    comic = models.FileItem.objects.get(
        file_type=models.FileItem.COMIC, parent=comic_directory
    )

    url = shortcuts.reverse("reader:read_comic", kwargs={"comic_id": comic.id})
    response = client.get(url)

    assert response.status_code == 200
    assert response.context["comic_id"] == comic.id
    assert response.context["previous_page_number"] == -1
    assert response.context["next_page_number"] == 1
    assert response.context["parent_id"] == comic_directory.id
    assert response.context["num_pages"] == 3
    assert response.context["current_page_number"] == 0
    assert response.context["current_page_width"] == 100


def test_comic_detail_spa(client):
    comic_directory = models.FileItem.objects.get(
        file_type=models.FileItem.DIRECTORY, parent__isnull=False
    )
    comic = models.FileItem.objects.get(
        file_type=models.FileItem.COMIC, parent=comic_directory
    )

    url = shortcuts.reverse("reader:read_comic_spa", kwargs={"comic_id": comic.id})
    response = client.get(url)

    assert response.status_code == 200
    comic_data = json.loads(response.context["comic_data_json"])
    assert comic_data["comicId"] == comic.id
    assert comic_data["numPages"] == 3
    assert comic_data["parentDirectoryUrl"] == shortcuts.reverse(
        "reader:directory", kwargs={"fileitem_id": comic_directory.id}
    )


def test_comic_detail_spa_with_no_next_comic(client):
    comic_directory = models.FileItem.objects.get(
        file_type=models.FileItem.DIRECTORY, parent__isnull=False
    )
    comic = models.FileItem.objects.get(
        file_type=models.FileItem.COMIC, parent=comic_directory
    )

    url = shortcuts.reverse("reader:read_comic_spa", kwargs={"comic_id": comic.id})
    response = client.get(url)

    comic_data = json.loads(response.context["comic_data_json"])
    assert comic_data["nextComic"] is None


def test_comic_detail_spa_with_next_comic(client):
    comic_directory = models.FileItem.objects.get(
        file_type=models.FileItem.DIRECTORY, parent__isnull=False
    )
    comic = models.FileItem.objects.get(
        file_type=models.FileItem.COMIC, parent=comic_directory
    )
    next_comic = models.FileItem.objects.create(
        name="02 - The Next Comic.cbz",
        path="/fake/02 - The Next Comic.cbz",
        file_type=models.FileItem.COMIC,
        parent=comic_directory,
    )

    url = shortcuts.reverse("reader:read_comic_spa", kwargs={"comic_id": comic.id})
    response = client.get(url)

    comic_data = json.loads(response.context["comic_data_json"])
    assert comic_data["nextComic"] == {
        "name": next_comic.name,
        "url": shortcuts.reverse(
            "reader:read_comic_spa", kwargs={"comic_id": next_comic.id}
        )
        + "?page_number=0",
    }


def test_comic_detail_spa_ignores_sibling_directories(client):
    comic_directory = models.FileItem.objects.get(
        file_type=models.FileItem.DIRECTORY, parent__isnull=False
    )
    comic = models.FileItem.objects.get(
        file_type=models.FileItem.COMIC, parent=comic_directory
    )
    # A sibling directory sorted after the comic must not be considered
    # the "next comic" — only siblings of type COMIC count.
    models.FileItem.objects.create(
        name="zzz - A Subdirectory",
        path="/fake/zzz - A Subdirectory",
        file_type=models.FileItem.DIRECTORY,
        parent=comic_directory,
    )

    url = shortcuts.reverse("reader:read_comic_spa", kwargs={"comic_id": comic.id})
    response = client.get(url)

    comic_data = json.loads(response.context["comic_data_json"])
    assert comic_data["nextComic"] is None


def test_update_comic_progress(client):
    comic_directory = models.FileItem.objects.get(
        file_type=models.FileItem.DIRECTORY, parent__isnull=False
    )
    comic = models.FileItem.objects.get(
        file_type=models.FileItem.COMIC, parent=comic_directory
    )

    url = shortcuts.reverse(
        "reader:update_comic_progress", kwargs={"comic_id": comic.id}
    )
    response = client.post(
        url,
        data=json.dumps({"page_number": 1}),
        content_type="application/json",
    )

    assert response.status_code == 200
    comic.refresh_from_db()
    assert comic.furthest_read_page == 1


def test_in_progress_view_orders_by_updated_at_desc(client):
    comic_directory = models.FileItem.objects.get(
        file_type=models.FileItem.DIRECTORY, parent__isnull=False
    )
    now = timezone.now()
    older = models.FileItem.objects.create(
        name="01 - Older.cbz",
        path="/fake/01 - Older.cbz",
        file_type=models.FileItem.COMIC,
        parent=comic_directory,
        furthest_read_page=1,
        is_read=False,
        updated_at=now - datetime.timedelta(hours=2),
    )
    newer = models.FileItem.objects.create(
        name="02 - Newer.cbz",
        path="/fake/02 - Newer.cbz",
        file_type=models.FileItem.COMIC,
        parent=comic_directory,
        furthest_read_page=1,
        is_read=False,
        updated_at=now,
    )
    # A comic with no updated_at (never touched since the field was
    # added) should still appear, but after the ones with a value.
    never_updated = models.FileItem.objects.create(
        name="03 - Never Updated.cbz",
        path="/fake/03 - Never Updated.cbz",
        file_type=models.FileItem.COMIC,
        parent=comic_directory,
        furthest_read_page=1,
        is_read=False,
        updated_at=None,
    )

    url = shortcuts.reverse("reader:in_progress")
    response = client.get(url)

    assert response.status_code == 200
    comics = list(response.context["comics"])
    assert comics == [newer, older, never_updated]


def test_set_furthest_read_page_bumps_updated_at(client):
    comic_directory = models.FileItem.objects.get(
        file_type=models.FileItem.DIRECTORY, parent__isnull=False
    )
    comic = models.FileItem.objects.get(
        file_type=models.FileItem.COMIC, parent=comic_directory
    )
    assert comic.updated_at is None

    comic.set_furthest_read_page(1)

    comic.refresh_from_db()
    assert comic.updated_at is not None
