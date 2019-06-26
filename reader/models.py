import os
from zipfile import ZipFile

from django.conf import settings
from django.db import models
from django.utils import http
from django.utils.functional import cached_property

from rarfile import RarFile


class FileItem(models.Model):
    COMIC = "comic"
    DIRECTORY = "directory"
    FILE_TYPE_CHOICES = ((COMIC, COMIC), (DIRECTORY, DIRECTORY))

    name = models.CharField(max_length=512, blank=True)
    path = models.TextField(blank=True)
    file_type = models.CharField(max_length=12, choices=FILE_TYPE_CHOICES, blank=True)

    parent = models.ForeignKey(
        "FileItem",
        related_name="children",
        on_delete=models.CASCADE,
        null=True,
        blank=True,
    )

    class Meta:
        ordering = ["-file_type", "name"]

    def __str__(self):
        return self.name

    def set_name(self):
        self.name = self.path.split("/")[-1]
        self.save()

    def set_file_type(self):
        if os.path.isdir(self.path):
            self.file_type = self.DIRECTORY
        else:
            self.file_type = self.COMIC
        self.save()

    def bookmark_page(self, page_number):
        """
        Create or update and existing bookmark for this comic
        on the given page number.
        """
        if self.file_type == self.COMIC:
            bookmark, created = Bookmark.objects.get_or_create(
                comic_id=self.pk, title=self.name
            )
            bookmark.page_num = page_number
            bookmark.save(update_fields=["page_num"])
        else:
            raise Exception(
                "Can't bookmark a page on a non-comic FileItem object ({})".format(
                    self.file_type
                )
            )

    @property
    def is_root(self):
        return self.path == settings.COMICS_ROOT

    @property
    def encoded_path(self):
        encoded_path = http.urlsafe_base64_encode(bytes(self.path, "utf-8"))
        encoded_path = encoded_path.decode("utf-8").replace("\n", "")
        return encoded_path

    @cached_property
    def num_pages(self):
        if self.file_type == self.COMIC:
            # Initialise the cb_file. This will raise a FileNotFoundError if
            # zipfile/rarfile can't find the file.
            if self.name.endswith(".cbz"):
                self.cb_file = ZipFile(self.path)
            else:
                self.cb_file = RarFile(self.path)

            # Set all the page names in order
            all_pages = [
                p
                for p in self.cb_file.namelist()
                if p.endswith(".jpg") or p.endswith(".jpeg") or p.endswith(".png")
            ]
            # Remove hidden files (files that start with `.`) from the pages list.
            all_pages = list(
                filter(lambda x: not x.split("/")[-1].startswith("."), all_pages)
            )
            return len(all_pages)
        return 0


class Bookmark(models.Model):
    """
    Model to keep track of the active page in a comic.
    """

    page_num = models.IntegerField()
    comic = models.ForeignKey("FileItem", on_delete=models.CASCADE)

    def __str__(self):
        return "Page %d on %s".format(self.page_num, self.comic.name)


class Favorite(models.Model):
    """
    Model to keep track of favorite comic directories.
    """

    title = models.CharField(max_length=128)
    directory_path = models.CharField(max_length=512)

    class Meta:
        ordering = ["title"]

    def __str__(self):
        return self.title
