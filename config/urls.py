# config/urls.py
"""
URL configuration for config project.
"""

from django.contrib import admin
from django.urls import path

from drf_yasg import openapi
from drf_yasg.views import get_schema_view
from rest_framework import permissions

schema_view = get_schema_view(
    openapi.Info(
        title="API Documentation",
        default_version="v1",
        description="API Documentation for Bulletin Board",
        terms_of_service="https://www.google.com/policies/terms/",
        contact=openapi.Contact(email="stasm226@gmail.com"),
        license=openapi.License(name="BSD License"),
    ),
    public=True,
    permission_classes=[permissions.AllowAny],
)


urlpatterns = [
    path("admin/", admin.site.urls),
    # -- Документация
    path("doc/", schema_view.with_ui("swagger", cache_timeout=0), name="schema-swagger-ui"),
    path("docjson/", schema_view.without_ui(cache_timeout=0), name="schema-json"),  # API без UI
    path("redoc/", schema_view.with_ui("redoc", cache_timeout=0), name="schema-redoc"),
]
