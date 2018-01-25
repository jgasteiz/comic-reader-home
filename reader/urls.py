from django.urls import path

from . import api
from . import views


app_name = 'reader'


urlpatterns = [
    path('', views.directory_detail, name='global_index'),
    path('dir/<str:directory_path>/', views.directory_detail, name='directory_detail'),
    path('comic/<str:comic_path>/<int:page_number>/', views.comic_detail, name='comic_detail'),
    path('delete_bookmark/', views.delete_bookmark, name='delete_bookmark'),

    # API
    path('api/comic/<str:comic_path>/<int:page_number>/', api.comic_page, name='api_comic_page'),
    path('api/directory/<str:directory_path>/', api.directory, name='api_directory'),
    path('api/bookmark/', api.bookmark_comic_page, name='bookmark_comic_page'),
]
