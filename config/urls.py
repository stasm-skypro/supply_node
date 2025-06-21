# config/urls.py
"""
URL configuration for config project.
"""

from django.contrib import admin
from django.http import HttpResponseRedirect
from django.urls import include, path

from drf_yasg import openapi
from drf_yasg.views import get_schema_view
from rest_framework import permissions

schema_view = get_schema_view(
    openapi.Info(
        title="API Documentation",
        default_version="v1",
        description="API Documentation for Supply Node",
        terms_of_service="https://www.google.com/policies/terms/",
        contact=openapi.Contact(email="stasm226@gmail.com"),
        license=openapi.License(name="BSD License"),
    ),
    public=True,
    permission_classes=[permissions.AllowAny],
    authentication_classes=[],
)


urlpatterns = [
    path("admin/", admin.site.urls),
    #
    path("doc/", schema_view.with_ui("swagger", cache_timeout=0), name="schema-swagger-ui"),
    path("docjson/", schema_view.without_ui(cache_timeout=0), name="schema-json"),  # API без UI
    path("redoc/", schema_view.with_ui("redoc", cache_timeout=0), name="schema-redoc"),
    #
    path("", lambda request: HttpResponseRedirect("doc/")),  # Чтобы при входе на / не было 404, редирект на doc/
    #
    path("user/", include("user.urls", namespace="user")),
    path("api-auth/", include("rest_framework.urls")),  # login/logout через API в браузере
    #
    path("supply/", include("supply.urls", namespace="supply")),
]
