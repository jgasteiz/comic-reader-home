from django.urls import path
from rest_framework import routers

from .views import api, public

router = routers.DefaultRouter()
router.register(r"fileitems", api.FileItemViewSet)

app_name = "reader"


urlpatterns = [
    path("", public.directory, name="directory"),
    path("dir/<int:fileitem_id>/", public.directory, name="directory"),
    path("comic/<int:comic_id>/", public.read_comic_page, name="read_comic_page",),
    path(
        "comic_page/<int:comic_id>/<int:page_number>/",
        public.comic_page_src,
        name="comic_page_src",
    ),
]
