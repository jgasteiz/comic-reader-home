from django.db import models


class Bookmark(models.Model):
    title = models.CharField(max_length=128, blank=True)
    comic_path = models.CharField(max_length=512)
    page_num = models.IntegerField(null=True)
