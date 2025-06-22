from django.urls import path

from supply.apps import SupplyConfig
from supply.views import (
    NodeCreateAPIView,
    NodeDestroyAPIView,
    NodeListAPIView,
    NodeProductListAPIView,
    NodeProductRetrieveAPIView,
    NodeRetrieveAPIView,
    NodeUpdateAPIView,
    ProductCreateAPI,
    ProductDestroyAPIView,
    ProductListAPI,
    ProductRetrieveAPIView,
    ProductUpdateAPIView,
)

app_name = SupplyConfig.name

urlpatterns = [
    path("nodes/", NodeListAPIView.as_view(), name="node-list"),
    path("nodes/create/", NodeCreateAPIView.as_view(), name="node-create"),
    path("nodes/<int:pk>/", NodeRetrieveAPIView.as_view(), name="node-detail"),
    path("nodes/<int:pk>/update/", NodeUpdateAPIView.as_view(), name="node-update"),
    path("nodes/<int:pk>/delete/", NodeDestroyAPIView.as_view(), name="node-delete"),
    #
    path("products/", ProductListAPI.as_view(), name="product-list"),
    path("products/create/", ProductCreateAPI.as_view(), name="product-create"),
    path("products/<int:pk>/", ProductRetrieveAPIView.as_view(), name="product-detail"),
    path("products/<int:pk>/update/", ProductUpdateAPIView.as_view(), name="product-update"),
    path("products/<int:pk>/delete/", ProductDestroyAPIView.as_view(), name="product-delete"),
    #
    path("nodes/<int:node_id>/products/", NodeProductListAPIView.as_view(), name="node-product-list"),
    path(
        "nodes/<int:node_id>/products/<int:product_id>/",
        NodeProductRetrieveAPIView.as_view(),
        name="node-product-detail",
    ),
]
