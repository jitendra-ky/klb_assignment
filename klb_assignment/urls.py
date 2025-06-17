"""project URL Configuration."""

from django.contrib import admin
from django.urls import include, path

urlpatterns = [
    path("admin/", admin.site.urls),

    path("", include("users.urls")),  # Include URLs from the users app
]
