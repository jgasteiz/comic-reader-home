from django.urls import path

from . import views


app_name = 'reader'


urlpatterns = [
    path('', views.directory_detail, name='global_index'),
    path('dir/<str:directory_path>/', views.directory_detail, name='directory_detail'),
    path('comic/<str:comic_path>/', views.comic_detail, name='comic_detail'),
]
