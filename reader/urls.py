from django.urls import path

from . import views


app_name = 'reader'


urlpatterns = [
    path('', views.global_index, name='global_index'),
    path('<str:comic_section>/', views.comic_index, name='comic_index'),
    path('detail/<str:comic_path>/', views.comic_detail, name='comic_detail'),
]
