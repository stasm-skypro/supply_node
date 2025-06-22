from django.urls import reverse

import pytest
from rest_framework import status
from rest_framework.test import APIClient

from user.models import User


@pytest.mark.django_db
class TestUserRegistration:
    """
    Тесты для регистрации пользователя.
    """

    def setup_method(self):
        """
        Создание клиента и URL для регистрации пользователя.
        :return:
        """
        self.client = APIClient()
        self.url = reverse("user:register")

    def test_successful_registration(self):
        """
        Тест успешной регистрации пользователя.
        :return:
        """
        data = {
            "first_name": "Иван",
            "last_name": "Иванов",
            "phone": "79999999999",
            "email": "test@example.com",
            "password": "secure1234",
            "password_confirmation": "secure1234",
        }
        response = self.client.post(self.url, data)
        assert response.status_code == status.HTTP_201_CREATED
        assert "message" in response.data
        assert User.objects.filter(email="test@example.com").exists()

    def test_duplicate_email(self):
        """
        Тест на дублирование email.
        :return:
        """
        User.objects.create_user(
            email="test@example.com", password="secure1234", first_name="Иван", last_name="Иванов", phone="79999999999"
        )
        data = {
            "first_name": "Петр",
            "last_name": "Петров",
            "phone": "79999999998",
            "email": "test@example.com",
            "password": "secure1234",
            "password_confirmation": "secure1234",
        }
        response = self.client.post(self.url, data)
        assert response.status_code == status.HTTP_400_BAD_REQUEST

    def test_password_mismatch(self):
        """
        Тест на несовпадение паролей.
        :return:
        """
        data = {
            "first_name": "Мария",
            "last_name": "Сидорова",
            "phone": "79999999997",
            "email": "mismatch@example.com",
            "password": "secure1234",
            "password_confirmation": "wrong1234",
        }
        response = self.client.post(self.url, data)
        assert response.status_code == status.HTTP_400_BAD_REQUEST
        assert "Пароли не совпадают!" in str(response.data)


@pytest.mark.django_db
class TestUserLogin:
    """
    Тесты для логина пользователя.
    """

    def setup_method(self):
        """
        Создание клиента и URL для логина пользователя.
        :return:
        """
        self.client = APIClient()
        self.url = reverse("user:token_obtain_pair")
        self.user = User.objects.create_user(
            email="user@example.com", password="secure1234", first_name="Имя", last_name="Фамилия", phone="70000000000"
        )

    def test_successful_login(self):
        """
        Тест успешного логина пользователя.
        :return:
        """
        data = {
            "email": "user@example.com",
            "password": "secure1234",
        }
        response = self.client.post(self.url, data)
        assert response.status_code == status.HTTP_200_OK
        assert "access" in response.data
        assert "refresh" in response.data

    def test_login_invalid_credentials(self):
        """
        Тест неверных учетных данных.
        :return:
        """
        data = {
            "email": "user@example.com",
            "password": "wrongpassword",
        }
        response = self.client.post(self.url, data)
        assert response.status_code == status.HTTP_401_UNAUTHORIZED
