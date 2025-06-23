# supply/views.py
"""
Представления для модели :class:`supply.models.Node`.

Этот модуль предоставляет набор представлений API на базе
:mod:`rest_framework.generics` для выполнения операций CRUD
(Create, Retrieve, Update, Delete) над моделью :class:`supply.models.Node`.
"""
import logging

from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import generics
from rest_framework.exceptions import NotFound
from rest_framework.permissions import IsAuthenticated

from supply.models import Node, Product
from supply.serializers import NodeSerializer, ProductSerializer

logger = logging.getLogger(__name__)


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

    def perform_create(self, serializer):
        instance = serializer.save()
        logger.info("Узел поставки создан: id=%s name='%s'", instance.id, instance.name)


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
        instance = serializer.save()
        logger.info("Узел поставки обновлён: id=%s name='%s'", instance.id, instance.name)


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

    def perform_destroy(self, instance):
        logger.info("Узел поставки удалён: id=%s name='%s'", instance.id, instance.name)
        super().perform_destroy(instance)


class ProductCreateAPI(generics.CreateAPIView):
    """
    Представление для создания нового продукта.

    Обрабатывает POST-запросы для создания экземпляров :class:`supply.models.Product`.
    Наследуется от :class:`rest_framework.generics.CreateAPIView`.

    Требует аутентификации пользователя.
    """

    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    permission_classes = [IsAuthenticated]

    def perform_create(self, serializer):
        instance = serializer.save()
        logger.info("Продукт создан: id=%s name='%s'", instance.id, instance.name)


class ProductListAPI(generics.ListAPIView):
    """
    Представление для получения списка всех продуктов.

    Обрабатывает GET-запросы для получения списка экземпляров :class:`supply.models.Product`.
    Поддерживает фильтрацию по полю ``owner`` (узел-владелец).

    Наследуется от :class:`rest_framework.generics.ListAPIView`.

    Требует аутентификации пользователя.
    """

    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    permission_classes = [IsAuthenticated]
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ["owner"]


class ProductRetrieveAPIView(generics.RetrieveAPIView):
    """
    Представление для получения одного продукта.

    Обрабатывает GET-запросы для получения экземпляра :class:`supply.models.Product` по его ``pk``.
    Наследуется от :class:`rest_framework.generics.RetrieveAPIView`.

    Требует аутентификации пользователя.
    """

    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    permission_classes = [IsAuthenticated]


class ProductUpdateAPIView(generics.UpdateAPIView):
    """
    Представление для обновления продукта.

    Обрабатывает PUT/PATCH-запросы для изменения экземпляра :class:`supply.models.Product`.
    Наследуется от :class:`rest_framework.generics.UpdateAPIView`.

    Требует аутентификации пользователя.
    """

    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    permission_classes = [IsAuthenticated]

    def perform_update(self, serializer):
        instance = serializer.save()
        logger.info("Продукт обновлён: id=%s name='%s'", instance.id, instance.name)


class ProductDestroyAPIView(generics.DestroyAPIView):
    """
    Представление для удаления продукта.

    Обрабатывает DELETE-запросы для удаления экземпляра :class:`supply.models.Product`.
    Наследуется от :class:`rest_framework.generics.DestroyAPIView`.

    Требует аутентификации пользователя.
    """

    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    permission_classes = [IsAuthenticated]

    def perform_destroy(self, instance):
        logger.info("Продукт удалён: id=%s name='%s'", instance.id, instance.name)
        super().perform_destroy(instance)


class NodeProductListAPIView(generics.ListAPIView):
    """
    Представление для получения списка продуктов, принадлежащих конкретному узлу сети.

    Обрабатывает GET-запросы по адресу ``/nodes/{node_id}/products/``.
    Возвращает список всех продуктов, у которых поле ``owner`` соответствует переданному ``node_id``.

    Наследуется от :class:`rest_framework.generics.ListAPIView`.

    Требует аутентификации пользователя.

    :param node_id: Уникальный идентификатор узла, переданный в URL.
    :type node_id: int
    :raises NotFound: Если узел с переданным ``node_id`` не найден.
    """

    serializer_class = ProductSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        """
        Получает список продуктов, принадлежащих указанному узлу.
        :return: Список продуктов.
        """
        node_id = self.kwargs.get("node_id")
        if not Node.objects.filter(pk=node_id).exists():
            raise NotFound(f"Узел с id={node_id} не найден.")
        return Product.objects.filter(owner_id=node_id)


class NodeProductRetrieveAPIView(generics.RetrieveAPIView):
    """
    Представление для получения конкретного продукта, принадлежащего узлу.

    Обрабатывает GET-запросы по адресу ``/nodes/{node_id}/products/{product_id}/``.
    Возвращает объект продукта, если он принадлежит указанному узлу.

    Наследуется от :class:`rest_framework.generics.RetrieveAPIView`.

    Требует аутентификации пользователя.

    :param node_id: Идентификатор узла, переданный в URL.
    :type node_id: int
    :param product_id: Идентификатор продукта, переданный в URL.
    :type product_id: int
    :raises NotFound: Если продукт с данным ``product_id`` не найден у узла с ``node_id``.
    """

    serializer_class = ProductSerializer
    permission_classes = [IsAuthenticated]

    def get_object(self):
        """
        Получает продукт по его ID и ID узла.

        :return: Экземпляр продукта, если найден.
        :rtype: supply.models.Product
        :raises NotFound: Если продукт не найден или не принадлежит указанному узлу.
        """
        node_id = self.kwargs.get("node_id")
        product_id = self.kwargs.get("product_id")

        try:
            return Product.objects.get(pk=product_id, owner_id=node_id)
        except Product.DoesNotExist:
            raise NotFound(f"Продукт с id={product_id} у узла id={node_id} не найден.")
