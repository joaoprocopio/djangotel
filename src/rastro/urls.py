from django.contrib import admin
from django.urls import include, path

from rastro.auth.presentation import urls as auth_urls

urlpatterns = [
    path("admin/", admin.site.urls),
    path("api/v1/auth/", include(auth_urls)),
]
