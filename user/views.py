# user/views.py
from rest_framework.generics import CreateAPIView
from rest_framework.permissions import AllowAny
from rest_framework_simplejwt.views import TokenObtainPairView

from user.serializers import EmailTokenObtainPairSerializer, RegisterSerializer  # type: ignore[reportUnusedImport]


class RegisterAPIView(CreateAPIView):
    """
    Регистрация нового пользователя.

    Атрибуты:
    - email (str): Email пользователя
    - phone (str): Контактный номер телефона пользователя
    - first_name (str): Имя пользователя
    - last_name (str): Фамилия пользователя
    - password (str): Пароль не менее 8 символов
    - password_confirmation (str): Подтверждение пароля

    Клиент отправляет POST-запрос на эндпоинт регистрации /register/,
    передавая JSON:
    ``json
    {
        "email": "user@example.com",
        "phone": "string",
        "first_name": "string",
        "last_name": "string",
        "password": "string",
        "password_confirmation": "string"
    }``

    API возвращает успешный ответ:
    ``json
    {
        "message": "Регистрация пользователя user@example.com прошла успешно."
    }
    ``
    """

    serializer_class = RegisterSerializer
    permission_classes = [AllowAny]

    def perform_create(self, serializer):
        """
        Сохраняет новый объект, используя переданный сериализатор

        Этот метод вызывается после успешной валидации данных.
        Здесь можно переопределить или расширить логику создания объекта,
        например, установить текущего пользователя в качестве владельца
        или выполнить дополнительные действия (логирование, отправка писем и т.п.).

        :param serializer: Валидированный сериализатор, содержащий данные для создания объекта
        :type serializer: rest_framework->serializers->Serializer
        """
        _ = serializer.save()
        # send_welcome_email.delay(user.email)  # type: ignore

    def create(self, request, *args, **kwargs):
        """
        Обрабатывает POST-запрос на создание нового объекта

        Метод вызывается при отправке POST-запроса к API-представлению, основанному на CreateAPIView.
        Валидирует входные данные, сохраняет новый объект и возвращает ответ с данными или сообщением.

        :param request: HTTP-запрос, содержащий входные данные (обычно JSON)
        :type request: rest_framework->request->Request
        :param args: Дополнительные позиционные аргументы
        :param kwargs: Дополнительные именованные аргументы
        :return: HTTP-ответ с сообщением об успешном создании объекта или ошибками валидации
        :rtype: rest_framework->response->Response
        """
        response = super().create(request, *args, **kwargs)
        email = request.data.get("email")
        response.data = {"message": f"Регистрация пользователя {email} прошла успешно."}
        return response


class EmailTokenObtainPairView(TokenObtainPairView):
    """
    Авторизация пользователя по email и паролю

    Клиент отправляет POST-запрос на эндпоинт аутентификации /login/,
    передавая JSON:
    ``json
    {
        "email": "user@example.com",
        "password": "secure1234",
    }
    ``

     API возвращает успешный ответ:
     ``json
    {
        "refresh": "eyJ...",
        "access": "eyJ..."
    }
    ``
    """

    serializer_class = EmailTokenObtainPairSerializer  # type: ignore[assignment]
