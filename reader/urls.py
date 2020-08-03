from django.urls import path

from . import views

app_name = "reader"


urlpatterns = [
    path("", views.directory, name="directory"),
    path("dir/<int:fileitem_id>/", views.directory, name="directory"),
    path("comic/<int:comic_id>/", views.read_comic_page, name="read_comic_page",),
    path(
        "comic_page/<int:comic_id>/<int:page_number>/",
        views.comic_page_src,
        name="comic_page_src",
    ),
]
