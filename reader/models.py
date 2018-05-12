import os

from django.conf import settings
from django.db import models


class FileItem(models.Model):
    COMIC = 'comic'
    DIRECTORY = 'directory'
    FILE_TYPE_CHOICES = (
        (COMIC, COMIC),
        (DIRECTORY, DIRECTORY),
    )

    name = models.CharField(max_length=512, blank=True)
    path = models.TextField(blank=True)
    file_type = models.CharField(max_length=12, choices=FILE_TYPE_CHOICES, blank=True)

    parent = models.ForeignKey('FileItem', related_name='children', on_delete=models.CASCADE, null=True)

    class Meta:
        ordering = ['-file_type', 'name']

    def __str__(self):
        return '%s - %s' % (self.file_type, self.name)

    def save(self, *args, **kwargs):
        # Set the directory name
        self.name = self.path.split('/')[-1]
        # Set the file type
        self.file_type = self.DIRECTORY if os.path.isdir(self.path) else self.COMIC
        super(FileItem, self).save(*args, **kwargs)

    @property
    def is_root(self):
        return self.path == settings.COMICS_ROOT

    @property
    def encoded_path(self):
        from reader.utils import get_encoded_path
        return get_encoded_path(self.path)


class Bookmark(models.Model):
    """
    Model to keep track of the active page in a comic.
    """
    title = models.CharField(max_length=128)
    comic_path = models.CharField(max_length=512)
    page_num = models.IntegerField(null=True)

    def __str__(self):
        return self.title


class Favorite(models.Model):
    """
    Model to keep track of favorite comic directories.
    """
    title = models.CharField(max_length=128)
    directory_path = models.CharField(max_length=512)

    class Meta:
        ordering = ['title']

    def __str__(self):
        return self.title
