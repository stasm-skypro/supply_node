# user/urls.py
from django.urls import path

from rest_framework_simplejwt.views import TokenRefreshView

from user.apps import UserConfig
from user.views import EmailTokenObtainPairView, RegisterAPIView

app_name = UserConfig.name

urlpatterns = [
    path("register/", RegisterAPIView.as_view(), name="register"),  # регистрация пользователя
    path("login/", EmailTokenObtainPairView.as_view(), name="token_obtain_pair"),  # логин
    path("token/refresh/", TokenRefreshView.as_view(), name="token_refresh"),  # обновление токена
]
