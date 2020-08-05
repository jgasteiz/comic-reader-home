from django.urls import path

from . import views

app_name = "reader"


urlpatterns = [
    # Directory views
    path("", views.directory, name="directory"),
    path("dir/<int:fileitem_id>/", views.directory, name="directory"),
    # Comic view
    path("comic/<int:comic_id>/read/", views.read_comic_page, name="read_comic_page",),
    # Page detail view
    path(
        "comic_page/<int:comic_id>/<int:page_number>/",
        views.comic_page_src,
        name="comic_page_src",
    ),
    # Comic operations
    path(
        "comic/<int:comic_id>/mark_as_unread/",
        views.mark_as_unread,
        name="mark_as_unread",
    ),
    path("comic/<int:comic_id>/mark_as_read/", views.mark_as_read, name="mark_as_read"),
    path(
        "comic/<int:directory_id>/mark_all_as_read/",
        views.mark_all_as_read,
        name="mark_all_as_read",
    ),
]
