from django.urls import path

from . import views


app_name = 'reader'


urlpatterns = [
    path('', views.comic_index, name='comic_index'),
    path('detail/<str:file_name>/', views.comic_detail, name='comic_detail'),
]
