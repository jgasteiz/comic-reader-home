from django.contrib import admin

from .models import Bookmark, Favorite, FileItem

admin.site.register(Bookmark)
admin.site.register(Favorite)
admin.site.register(FileItem)
