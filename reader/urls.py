from django.urls import path

from . import api
from . import views


app_name = 'reader'


urlpatterns = [
    # API
    path('api/comic/<str:comic_path>/', api.comic_detail, name='api_comic_detail'),
    path('api/page/<str:comic_path>/<int:page_number>/', api.comic_page_src, name='api_comic_page_src'),
    path('api/directory/', api.directory_view, name='api_directory_root'),
    path('api/directory/<str:directory_path>/', api.directory_view, name='api_directory'),
    path('api/bookmark/', api.bookmark_comic_page, name='bookmark_comic_page'),

    path('', views.comic_reader, name='comic_reader'),
    path('dir/<str:directory_path>/', views.comic_reader, name='comic_reader'),
    path('comic/<str:comic_path>/', views.comic_reader, name='comic_reader'),
    path('comic/<str:comic_path>/<int:page_number>/', views.comic_reader, name='comic_reader'),
]
