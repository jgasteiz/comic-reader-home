from django.urls import path

from . import api
from . import views


app_name = 'reader'


urlpatterns = [
    path('', views.directory_detail, name='global_index'),
    path('dir/<str:directory_path>/', views.directory_detail, name='directory_detail'),
    path('comic/<str:comic_path>/<int:page_number>/', views.comic_detail, name='comic_detail'),

    # API
    path('api/<str:comic_path>/<int:page_number>/', api.comic_page, name='comic_page'),
    path('api/bookmark/', api.bookmark_comic_page, name='bookmark_comic_page'),
]
