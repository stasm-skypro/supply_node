from django.urls import reverse

import pytest
from rest_framework import status
from rest_framework.test import APIClient

from user.models import User


@pytest.mark.django_db
class TestUserRegistration:
    """
    Набор тестов для регистрации пользователя.

    Содержит интеграционные тесты для эндпоинта регистрации пользователя.

    Эндпоинт: ``/user/register/``
    """

    def setup_method(self):
        """
        Подготовка клиента и URL регистрации.

        :return: None
        """
        self.client = APIClient()
        self.url = reverse("user:register")

    def test_successful_registration(self):
        """
        Проверка успешной регистрации пользователя.

        Отправляется корректный POST-запрос. Проверяется, что возвращается
        статус 201 и пользователь сохраняется в базе данных.

        :return: None
        :rtype: None
        :raises AssertionError: Если код ответа или данные в базе некорректны.
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
        Проверка регистрации с уже существующим email.

        При попытке регистрации с email, который уже существует в базе,
        ожидается ответ 400 BAD REQUEST.

        :return: None
        :rtype: None
        :raises AssertionError: Если возвращается некорректный код ответа.
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
        Проверка регистрации при несовпадении паролей.

        Если пароль и подтверждение пароля не совпадают,
        должен возвращаться ответ 400 BAD REQUEST с соответствующей ошибкой.

        :return: None
        :rtype: None
        :raises AssertionError: Если код ответа или сообщение об ошибке некорректны.
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
    Набор тестов для входа пользователя (JWT-аутентификация).

    Содержит тесты на получение access и refresh токенов.

    Эндпоинт: ``/user/token/``
    """

    def setup_method(self):
        """
        Подготовка клиента, URL входа и создание тестового пользователя.

        :return: None
        """
        self.client = APIClient()
        self.url = reverse("user:token_obtain_pair")
        self.user = User.objects.create_user(
            email="user@example.com", password="secure1234", first_name="Имя", last_name="Фамилия", phone="70000000000"
        )

    def test_successful_login(self):
        """
        Проверка успешного входа пользователя.

        Отправляется корректный email и пароль.
        Ожидается ответ 200 OK и наличие токенов в ответе.

        :return: None
        :rtype: None
        :raises AssertionError: Если отсутствуют токены или неверный код ответа.
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
        Проверка входа с неверными данными.

        При вводе неправильного пароля должен вернуться статус 401 UNAUTHORIZED.

        :return: None
        :rtype: None
        :raises AssertionError: Если возвращён неправильный код ответа.
        """
        data = {
            "email": "user@example.com",
            "password": "wrongpassword",
        }
        response = self.client.post(self.url, data)
        assert response.status_code == status.HTTP_401_UNAUTHORIZED
