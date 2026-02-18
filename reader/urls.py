from django.urls import path

from . import views

app_name = "reader"


urlpatterns = [
    # Directory views
    path("", views.directory, name="directory"),
    path("directory/<int:fileitem_id>/", views.directory, name="directory"),
    # Comic view
    path(
        "comic/<int:comic_id>/",
        views.page,
        name="read_comic",
    ),
    # SPA comic view
    path(
        "comic/<int:comic_id>/spa/",
        views.page_spa,
        name="read_comic_spa",
    ),
    # Comic progress update (for SPA)
    path(
        "comic/<int:comic_id>/progress/",
        views.update_comic_progress,
        name="update_comic_progress",
    ),
    # Page detail view
    path(
        "comic/<int:comic_id>/page/<int:page_number>/",
        views.page_src,
        name="page_src",
    ),
    # Comic operations
    path(
        "comic/<int:comic_id>/mark_as_unread/",
        views.mark_comic_as_unread,
        name="mark_as_unread",
    ),
    path(
        "comic/<int:comic_id>/mark_as_read/",
        views.mark_comic_as_read,
        name="mark_as_read",
    ),
    path(
        "comic/<int:directory_id>/mark_all_as_read/",
        views.mark_directory_as_read,
        name="mark_all_as_read",
    ),
]
