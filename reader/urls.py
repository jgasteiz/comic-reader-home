from django.urls import path, include
from rest_framework import routers

from reader.views.api import FileItemViewSet
from .views import old_api, public

router = routers.DefaultRouter()
router.register(r'fileitems', FileItemViewSet)

app_name = 'reader'


urlpatterns = [
    # API
    path('api/directory/', old_api.directory_view, name='api_directory_root'),
    path('api/directory/<str:directory_path>/', old_api.directory_view, name='api_directory'),
    path('api/comic/<str:comic_path>/', old_api.comic_detail, name='api_comic_detail'),
    path('api/page/<str:comic_path>/<int:page_number>/', old_api.comic_page_src, name='api_comic_page_src'),
    path('api/bookmark/', old_api.bookmark_comic_page, name='bookmark_comic_page'),

    # API v2
    path('apiv2/', include(router.urls)),

    # Public views
    path('', public.home, name='home'),
    path('dir/<int:fileitem_id>/', public.home, name='home'),
    path('comic/<int:fileitem_id>/', public.home, name='home'),
    path('comic/<int:fileitem_id>/<int:page_number>/', public.home, name='home'),
]
