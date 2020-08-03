from django.contrib import admin
from django.urls import include, path

from reader import urls as reader_urls

urlpatterns = [
    path("admin/", admin.site.urls),
    path("api-auth/", include("rest_framework.urls")),
    path("", include(reader_urls, namespace="reader")),
]
