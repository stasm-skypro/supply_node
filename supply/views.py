# supply/views.py
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import generics
from rest_framework.permissions import IsAuthenticated

from supply.models import Node
from supply.serializers import NodeSerializer


# -- CREATE
class NodeCreateAPIView(generics.CreateAPIView):
    queryset = Node.objects.all()
    serializer_class = NodeSerializer
    permission_classes = [IsAuthenticated]


# -- LIST с фильтрацией по стране
class NodeListAPIView(generics.ListAPIView):
    queryset = Node.objects.all()
    serializer_class = NodeSerializer
    permission_classes = [IsAuthenticated]
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ["country"]


# -- RETRIEVE
class NodeRetrieveAPIView(generics.RetrieveAPIView):
    queryset = Node.objects.all()
    serializer_class = NodeSerializer
    permission_classes = [IsAuthenticated]


# -- UPDATE (с запретом на обновление поля 'debt_to_supplier')
class NodeUpdateAPIView(generics.UpdateAPIView):
    queryset = Node.objects.all()
    serializer_class = NodeSerializer
    permission_classes = [IsAuthenticated]

    def perform_update(self, serializer):
        validated_data = serializer.validated_data
        validated_data.pop("debt_to_supplier", None)  # запрет на изменение
        serializer.save()


# -- DESTROY
class NodeDestroyAPIView(generics.DestroyAPIView):
    queryset = Node.objects.all()
    serializer_class = NodeSerializer
    permission_classes = [IsAuthenticated]
