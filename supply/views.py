# supply/views.py
"""
Представления (views) для модели Node.

Этот модуль содержит классы представлений Django Rest Framework для выполнения
операций CRUD (Create, Retrieve, Update, Delete) над моделью Node.
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

    Использует :class:`rest_framework.generics.CreateAPIView` для обработки POST-запросов
    и создания новых экземпляров модели :class:`supply.models.Node`.
    Требует аутентификации пользователя.
    """

    queryset = Node.objects.all()
    serializer_class = NodeSerializer
    permission_classes = [IsAuthenticated]


# -- LIST с фильтрацией по стране
class NodeListAPIView(generics.ListAPIView):
    """
    Представление для получения списка объектов сети (Node).

    Использует :class:`rest_framework.generics.ListAPIView` для обработки GET-запросов
    и возврата списка всех экземпляров модели :class:`supply.models.Node`.
    Поддерживает фильтрацию по полю 'country'.
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

    Использует :class:`rest_framework.generics.RetrieveAPIView` для обработки GET-запросов
    и возврата одного экземпляра модели :class:`supply.models.Node` по его 'pk'.
    Требует аутентификации пользователя.
    """

    queryset = Node.objects.all()
    serializer_class = NodeSerializer
    permission_classes = [IsAuthenticated]


# -- UPDATE (с запретом на обновление поля 'debt_to_supplier')
class NodeUpdateAPIView(generics.UpdateAPIView):
    """
    Представление для обновления объекта сети (Node).

    Использует :class:`rest_framework.generics.UpdateAPIView` для обработки PUT/PATCH-запросов
    и обновления экземпляра модели :class:`supply.models.Node`.

    **Особенность:** Запрещает обновление поля 'debt_to_supplier'.
    Требует аутентификации пользователя.
    """

    queryset = Node.objects.all()
    serializer_class = NodeSerializer
    permission_classes = [IsAuthenticated]

    def perform_update(self, serializer):
        """
        Выполняет обновление экземпляра, исключая поле 'debt_to_supplier'.

        Переопределяет стандартный метод для удаления поля 'debt_to_supplier'
        из валидированных данных перед сохранением.

        :param serializer: Сериализатор с валидированными данными.
        :type serializer: NodeSerializer
        """
        validated_data = serializer.validated_data
        validated_data.pop("debt_to_supplier", None)  # запрет на изменение
        serializer.save()


# -- DESTROY
class NodeDestroyAPIView(generics.DestroyAPIView):
    """
    Представление для удаления объекта сети (Node).

    Использует :class:`rest_framework.generics.DestroyAPIView` для обработки DELETE-запросов
    и удаления экземпляра модели :class:`supply.models.Node`.
    Требует аутентификации пользователя.
    """

    queryset = Node.objects.all()
    serializer_class = NodeSerializer
    permission_classes = [IsAuthenticated]
