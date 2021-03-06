from django.contrib import admin
from django.urls import reverse

from . import models


@admin.register(models.FileItem)
class FileItemAdmin(admin.ModelAdmin):
    list_filter = ("file_type",)
    search_fields = ("name",)

    def view_on_site(self, obj):
        if obj.file_type == models.FileItem.COMIC:
            return reverse("reader:comic", kwargs={"fileitem_id": obj.pk})
        else:
            return reverse("reader:dir", kwargs={"fileitem_id": obj.pk})
