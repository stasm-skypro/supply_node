from django.urls import path

from supply.apps import SupplyConfig
from supply.views import NodeCreateAPIView, NodeDestroyAPIView, NodeListAPIView, NodeRetrieveAPIView, NodeUpdateAPIView

app_name = SupplyConfig.name

urlpatterns = [
    path("nodes/", NodeListAPIView.as_view(), name="node-list"),
    path("nodes/create/", NodeCreateAPIView.as_view(), name="node-create"),
    path("nodes/<int:pk>/", NodeRetrieveAPIView.as_view(), name="node-detail"),
    path("nodes/<int:pk>/update/", NodeUpdateAPIView.as_view(), name="node-update"),
    path("nodes/<int:pk>/delete/", NodeDestroyAPIView.as_view(), name="node-delete"),
]
