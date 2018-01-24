from django.contrib import admin

from .models import Bookmark, Favorite

admin.site.register(Bookmark)
admin.site.register(Favorite)
