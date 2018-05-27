from django.urls import path, include
from rest_framework import routers

from .views import public, api

router = routers.DefaultRouter()
router.register(r'fileitems', api.FileItemViewSet)

app_name = 'reader'


urlpatterns = [
    # API
    path('api/', include(router.urls)),
    path('api/page/<int:comic_id>/<int:page_number>/', api.comic_page_src, name='api_comic_page_src'),
    path('api/bookmark/', api.bookmark_comic_page, name='bookmark_comic_page'),

    # Public views
    path('', public.home, name='root'),
    path('dir/<int:fileitem_id>/', public.home, name='dir'),
    path('comic/<int:fileitem_id>/', public.home, name='comic'),
    path('comic/<int:fileitem_id>/<int:page_number>/', public.home, name='comic'),
]
