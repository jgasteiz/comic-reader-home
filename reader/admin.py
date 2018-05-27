from django.contrib import admin
from django.urls import reverse

from .models import Bookmark, Favorite, FileItem


class FileItemAdmin(admin.ModelAdmin):
    list_filter = ('file_type',)
    search_fields = ('name',)

    def view_on_site(self, obj):
        if obj.file_type == FileItem.COMIC:
            return reverse('reader:comic', kwargs={'fileitem_id': obj.pk})
        else:
            return reverse('reader:dir', kwargs={'fileitem_id': obj.pk})


admin.site.register(Bookmark)
admin.site.register(Favorite)
admin.site.register(FileItem, FileItemAdmin)
