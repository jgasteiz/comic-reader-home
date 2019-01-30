from django.contrib import admin
from django.urls import reverse

from . import models


class FileItemAdmin(admin.ModelAdmin):
    list_filter = ('file_type',)
    search_fields = ('name',)

    def view_on_site(self, obj):
        if obj.file_type == models.FileItem.COMIC:
            return reverse('reader:comic', kwargs={'fileitem_id': obj.pk})
        else:
            return reverse('reader:dir', kwargs={'fileitem_id': obj.pk})


admin.site.register(models.Bookmark)
admin.site.register(models.Favorite)
admin.site.register(models.FileItem, FileItemAdmin)
