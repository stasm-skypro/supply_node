# supply/views.py
"""
Представления для модели :class:`supply.models.Node`.

Этот модуль предоставляет набор представлений API на базе
:mod:`rest_framework.generics` для выполнения операций CRUD
(Create, Retrieve, Update, Delete) над моделью :class:`supply.models.Node`.
"""
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import generics
from rest_framework.permissions import IsAuthenticated

from supply.models import Node
from supply.serializers import NodeSerializer


# -- CREATE
class NodeCreateAPIView(generics.CreateAPIView):
    """
    Представление для создания нового объекта сети (Node).

    Обрабатывает POST-запросы для создания экземпляров :class:`supply.models.Node`.
    Наследуется от :class:`rest_framework.generics.CreateAPIView`.

    Требует аутентификации пользователя.
    """

    queryset = Node.objects.all()
    serializer_class = NodeSerializer
    permission_classes = [IsAuthenticated]


# -- LIST с фильтрацией по стране
class NodeListAPIView(generics.ListAPIView):
    """
    Представление для получения списка объектов сети (Node).

    Обрабатывает GET-запросы для получения списка экземпляров :class:`supply.models.Node`.
    Наследуется от :class:`rest_framework.generics.ListAPIView`.

    Поддерживает фильтрацию по полю ``country``.
    Требует аутентификации пользователя.
    """

    queryset = Node.objects.all()
    serializer_class = NodeSerializer
    permission_classes = [IsAuthenticated]
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ["country"]


# -- RETRIEVE
class NodeRetrieveAPIView(generics.RetrieveAPIView):
    """
    Представление для получения одного объекта сети (Node).

    Обрабатывает GET-запросы для получения одного экземпляра :class:`supply.models.Node` по его ``pk``.
    Наследуется от :class:`rest_framework.generics.RetrieveAPIView`.

    Требует аутентификации пользователя.
    """

    queryset = Node.objects.all()
    serializer_class = NodeSerializer
    permission_classes = [IsAuthenticated]


# -- UPDATE (с запретом на обновление поля 'debt_to_supplier')
class NodeUpdateAPIView(generics.UpdateAPIView):
    """
    Представление для обновления объекта сети (Node).

    Обрабатывает PUT/PATCH-запросы для обновления экземпляра :class:`supply.models.Node`.
    Наследуется от :class:`rest_framework.generics.UpdateAPIView`.

    .. note::
        Обновление поля ``debt_to_supplier`` через API запрещено.
        Эта логика реализована в методе :meth:`~perform_update`.

    Требует аутентификации пользователя.
    """

    queryset = Node.objects.all()
    serializer_class = NodeSerializer
    permission_classes = [IsAuthenticated]

    def perform_update(self, serializer):
        """
        Выполняет обновление, исключая поле ``debt_to_supplier``.

        Этот метод переопределен, чтобы предотвратить изменение задолженности
        поставщику через API. Он удаляет поле ``debt_to_supplier`` из
        валидированных данных перед сохранением.

        :param serializer: Сериализатор с валидированными данными.
        :type serializer: supply.serializers.NodeSerializer
        """
        validated_data = serializer.validated_data
        validated_data.pop("debt_to_supplier", None)  # запрет на изменение
        serializer.save()


# -- DESTROY
class NodeDestroyAPIView(generics.DestroyAPIView):
    """
    Представление для удаления объекта сети (Node).

    Обрабатывает DELETE-запросы для удаления экземпляра :class:`supply.models.Node`.
    Наследуется от :class:`rest_framework.generics.DestroyAPIView`.

    Требует аутентификации пользователя.
    """

    queryset = Node.objects.all()
    serializer_class = NodeSerializer
    permission_classes = [IsAuthenticated]
