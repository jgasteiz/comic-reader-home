from django.db import models


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
