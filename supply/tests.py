from datetime import date

from django.urls import reverse

import pytest
from rest_framework import status
from rest_framework.test import APIClient

from supply.models import Node, Product
from user.models import User


@pytest.mark.django_db
class TestNodeEndpoints:
    """
    Тесты CRUD-операций над моделью Node через API.

    Используется фикстура базы данных для создания пользователя и проверки
    всех операций над звеньями сети поставок, включая создание, получение списка,
    получение по ID, обновление и удаление.
    """

    def setup_method(self):
        """
        Подготовка окружения для тестов Node.
        Создание клиента и авторизованного пользователя.
        """
        self.client = APIClient()
        self.user = User.objects.create_user(
            email="user@example.com", password="secure1234", first_name="Имя", last_name="Фамилия", phone="70000000000"
        )
        self.client.force_authenticate(user=self.user)

    def test_create_node(self):
        """
        Тест успешного создания узла сети.

        :returns: HTTP 201 и проверка наличия объекта в базе.
        """
        url = reverse("supply:node-create")
        data = {
            "name": "Завод 1",
            "email": "factory@example.com",
            "phone": "79000000000",
            "country": "Россия",
            "city": "Москва",
            "street": "Ленина",
            "building_number": "1",
        }
        response = self.client.post(url, data)
        assert response.status_code == status.HTTP_201_CREATED
        assert Node.objects.filter(name="Завод 1").exists()

    def test_list_nodes(self):
        """
        Тест получения списка узлов сети с фильтрацией по стране.

        :returns: HTTP 200 и проверка длины ответа.
        """
        Node.objects.create(
            name="Узел 1",
            email="a@a.com",
            phone="70000000001",
            country="Россия",
            city="Москва",
            street="Ленина",
            building_number="1",
        )
        url = reverse("supply:node-list") + "?country=Россия"
        response = self.client.get(url)
        assert response.status_code == status.HTTP_200_OK
        assert len(response.data) == 1

    def test_retrieve_node(self):
        """
        Тест получения одного узла по его идентификатору.

        :returns: HTTP 200 и проверка возвращаемого имени узла.
        """
        node = Node.objects.create(
            name="Узел 1",
            email="a@a.com",
            phone="70000000001",
            country="Россия",
            city="Москва",
            street="Ленина",
            building_number="1",
        )
        url = reverse("supply:node-detail", args=[node.pk])
        response = self.client.get(url)
        assert response.status_code == status.HTTP_200_OK
        assert response.data["name"] == "Узел 1"

    def test_update_node_exclude_debt(self):
        """
        Тест обновления узла с исключением поля `debt_to_supplier`.

        :returns: HTTP 200 и проверка того, что `debt_to_supplier` не изменился.
        """
        node = Node.objects.create(
            name="Узел",
            email="a@a.com",
            phone="70000000001",
            country="Казахстан",
            city="Алматы",
            street="Абая",
            building_number="1",
            debt_to_supplier=1000,
        )
        url = reverse("supply:node-update", args=[node.pk])
        response = self.client.patch(url, {"debt_to_supplier": 0})
        node.refresh_from_db()
        assert response.status_code == status.HTTP_200_OK
        assert str(node.debt_to_supplier) == "1000.00"

    def test_destroy_node(self):
        """
        Тест удаления узла.

        :returns: HTTP 204 и проверка отсутствия записи в базе.
        """
        node = Node.objects.create(
            name="Удаляемый",
            email="b@b.com",
            phone="70000000002",
            country="Россия",
            city="Казань",
            street="Горького",
            building_number="10",
        )
        url = reverse("supply:node-delete", args=[node.pk])
        response = self.client.delete(url)
        assert response.status_code == status.HTTP_204_NO_CONTENT
        assert not Node.objects.filter(pk=node.pk).exists()


@pytest.mark.django_db
class TestProductEndpoints:
    """
    Тесты CRUD-операций над моделью Product через API.

    Покрытие включает создание, список, получение по ID, обновление, удаление,
    а также вложенные маршруты по узлу: /nodes/{id}/products/ и /nodes/{id}/products/{id}/.
    """

    def setup_method(self):
        """
        Подготовка окружения: пользователь, клиент и один узел.
        """
        self.client = APIClient()
        self.user = User.objects.create_user(
            email="user@example.com", password="secure1234", first_name="Имя", last_name="Фамилия", phone="70000000000"
        )
        self.client.force_authenticate(user=self.user)
        self.node = Node.objects.create(
            name="Узел 1",
            email="z@z.com",
            phone="70000000010",
            country="Узбекистан",
            city="Ташкент",
            street="Навои",
            building_number="7",
        )

    def test_create_product(self):
        """
        Тест создания продукта.

        :returns: HTTP 201 и проверка названия продукта.
        """
        url = reverse("supply:product-create")
        data = {"name": "Товар", "model": "X123", "release_date": str(date.today()), "owner": self.node.pk}
        response = self.client.post(url, data)
        assert response.status_code == status.HTTP_201_CREATED
        assert Product.objects.filter(name="Товар").exists()

    def test_node_product_list(self):
        """
        Тест получения списка продуктов по узлу.

        :returns: HTTP 200 и проверка количества.
        """
        Product.objects.create(name="P1", model="M1", release_date=date.today(), owner=self.node)
        url = reverse("supply:node-product-list", kwargs={"node_id": self.node.pk})
        response = self.client.get(url)
        assert response.status_code == status.HTTP_200_OK
        assert len(response.data) == 1

    def test_node_product_retrieve(self):
        """
        Тест получения одного продукта по node_id и product_id.

        :returns: HTTP 200 и проверка названия продукта.
        """
        product = Product.objects.create(name="P1", model="M1", release_date=date.today(), owner=self.node)
        url = reverse("supply:node-product-detail", kwargs={"node_id": self.node.pk, "product_id": product.pk})
        response = self.client.get(url)
        assert response.status_code == status.HTTP_200_OK
        assert response.data["name"] == "P1"

    def test_update_product(self):
        """
        Тест обновления информации о продукте.

        :returns: HTTP 200 и проверка обновлённого поля.
        """
        product = Product.objects.create(name="Old", model="M", release_date=date.today(), owner=self.node)
        url = reverse("supply:product-update", args=[product.pk])
        response = self.client.patch(url, {"name": "New"})
        assert response.status_code == status.HTTP_200_OK
        product.refresh_from_db()
        assert product.name == "New"

    def test_destroy_product(self):
        """
        Тест удаления продукта.

        :returns: HTTP 204 и отсутствие записи в базе.
        """
        product = Product.objects.create(name="Удалить", model="M", release_date=date.today(), owner=self.node)
        url = reverse("supply:product-delete", args=[product.pk])
        response = self.client.delete(url)
        assert response.status_code == status.HTTP_204_NO_CONTENT
        assert not Product.objects.filter(pk=product.pk).exists()
