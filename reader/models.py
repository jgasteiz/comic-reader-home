import os

from django.conf import settings
from django.db import models


class FileItem(models.Model):
    COMIC = "comic"
    DIRECTORY = "directory"
    FILE_TYPE_CHOICES = ((COMIC, COMIC), (DIRECTORY, DIRECTORY))

    name = models.CharField(max_length=512, blank=True)
    path = models.TextField(blank=True)
    file_type = models.CharField(
        max_length=12, choices=FILE_TYPE_CHOICES, db_index=True
    )

    parent = models.ForeignKey(
        "FileItem",
        related_name="children",
        on_delete=models.CASCADE,
        null=True,
        blank=True,
    )

    furthest_read_page = models.IntegerField(null=True)
    is_read = models.BooleanField(default=False)

    class Meta:
        ordering = ["name"]

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

    def set_furthest_read_page(self, page_number):
        self.furthest_read_page = page_number
        # In case we've started re-reading a comic
        self.is_read = False
        self.save()

    def mark_as_read(self):
        self.is_read = True
        self.save()

    def mark_as_unread(self):
        self.furthest_read_page = None
        self.is_read = False
        self.save()

    @property
    def is_root(self):
        return self.path == settings.COMICS_SRC_PATH

    @property
    def is_comic(self):
        return self.file_type == self.COMIC
