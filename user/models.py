# user/models.py
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin
from django.db import models


class UserManager(BaseUserManager):
    """
    Определяет менеджер для кастомной модели User.

    Этот менеджер необходим для корректного создания обычных пользователей
    и суперпользователей через команды `createsuperuser` и в коде.
    """

    def create_user(self, email, password=None, **extra_fields):
        """
        Создаёт и сохраняет обычного пользователя с указанным email и паролем.

        :param email: Электронная почта пользователя. Должна быть уникальной.
        :type email: str
        :param password: Пароль пользователя.
        :type password: str, optional
        :param extra_fields: Дополнительные поля, передаваемые в модель пользователя.
        :type extra_fields: dict
        :raises ValueError: Если email не указан.
        :return: Созданный объект пользователя.
        :rtype: :class:`User`
        """
        if not email:
            raise ValueError("Email обязателен")
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password=None, **extra_fields):
        """
        Создаёт и сохраняет суперпользователя с указанным email и паролем.

        Суперпользователь автоматически получает права ``is_staff=True`` и ``is_superuser=True``.

        :param email: Электронная почта суперпользователя.
        :type email: str
        :param password: Пароль суперпользователя.
        :type password: str, optional
        :param extra_fields: Дополнительные поля, передаваемые в модель пользователя.
        :type extra_fields: dict
        :raises ValueError: Если ``is_staff`` или ``is_superuser`` не установлены в True.
        :return: Созданный объект суперпользователя.
        :rtype: :class:`User`
        """
        extra_fields.setdefault("is_staff", True)
        extra_fields.setdefault("is_superuser", True)

        if not extra_fields.get("is_staff"):
            raise ValueError("У суперпользователя должно быть is_staff=True.")
        if not extra_fields.get("is_superuser"):
            raise ValueError("У суперпользователя должно быть is_superuser=True.")
        return self.create_user(email, password, **extra_fields)


class User(AbstractBaseUser, PermissionsMixin):
    """
    Определяет кастомную модель пользователя для приложения.

    Пользователь в данном контексте - это не конечный клиент, а скорее
    управляющий интерфейсом приложения (например, администратор, поставщик,
    менеджер и т.д.).

    :ivar id: Уникальный идентификатор пользователя (PK).
    :vartype id: int
    :ivar email: Электронная почта. Используется как ``USERNAME_FIELD``.
    :vartype email: str
    :ivar phone: Контактный номер телефона.
    :vartype phone: str
    :ivar first_name: Имя пользователя.
    :vartype first_name: str
    :ivar last_name: Фамилия пользователя.
    :vartype last_name: str
    :ivar image: Аватар пользователя.
    :vartype image: django.db.models.ImageField
    :ivar role: Роль пользователя в системе (см. :class:`~User.Roles`).
    :vartype role: str
    :ivar is_active: Флаг активности пользователя. Неактивные не могут войти.
    :vartype is_active: bool
    :ivar is_staff: Флаг доступа к административной панели Django.
    :vartype is_staff: bool
    :ivar is_superuser: Флаг, дающий все права без их явного назначения.
    :vartype is_superuser: bool
    :ivar last_login: Дата и время последнего входа.
    :vartype last_login: datetime.datetime
    :ivar date_joined: Дата и время регистрации.
    :vartype date_joined: datetime.datetime
    """

    class Roles(models.TextChoices):
        """
        Определяет перечисление ролей пользователей в системе.

        Использование `TextChoices` обеспечивает безопасность типов,
        улучшает читаемость кода и упрощает поддержку.
        """

        USER = "user", "Пользователь"
        ADMIN = "admin", "Администратор"

    # Комменты '# type: ignore[var-annotated]' для mypy - чтобы не требовал аннотаций типов
    email = models.EmailField(
        unique=True,
        verbose_name="Email",
        help_text="Укажите адрес электронной почты",
        error_messages={"unique": "Пользователь с таким email уже существует."},
    )  # type: ignore[var-annotated]

    phone = models.CharField(
        max_length=20,
        blank=True,
        verbose_name="Номер телефона",
        help_text="Укажите номер телефона",
    )  # type: ignore[var-annotated]

    first_name = models.CharField(
        max_length=30,
        blank=True,
        verbose_name="Имя",
        help_text="Укажите имя",
    )  # type: ignore[var-annotated]

    last_name = models.CharField(
        max_length=30,
        blank=True,
        verbose_name="Фамилия",
        help_text="Укажите фамилию",
    )  # type: ignore[var-annotated]

    image = models.ImageField(
        upload_to="avatars/",
        verbose_name="Аватар",
        help_text="Загрузите аватар",
        blank=True,
        null=True,
    )  # type: ignore[var-annotated]

    role = models.CharField(
        max_length=20,
        choices=Roles.choices,
        default=Roles.USER,
        verbose_name="Роль",
        help_text="Укажите вашу роль",
    )  # type: ignore[var-annotated]

    is_active = models.BooleanField(
        default=True,
        verbose_name="Активен",
    )  # type: ignore[var-annotated]

    is_staff = models.BooleanField(
        default=False,
        verbose_name="Сотрудник",
    )  # type: ignore[var-annotated]

    is_superuser = models.BooleanField(
        default=False,
        verbose_name="Суперпользователь",
    )  # type: ignore[var-annotated]

    last_login = models.DateTimeField(
        auto_now=True,
        verbose_name="Последний вход",
    )  # type: ignore[var-annotated]

    date_joined = models.DateTimeField(
        auto_now_add=True,
        verbose_name="Дата регистрации",
    )  # type: ignore[var-annotated]

    objects = UserManager()

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = [
        "first_name",
        "last_name",
        "phone",
    ]

    id: int  # Для mypy, чтобы не требовал аннотаций

    def __str__(self):
        """
        Возвращает строковое представление пользователя.

        :return: Email пользователя.
        :rtype: str
        """
        return self.email

    class Meta:
        """
        Класс метаданных для модели User.

        Определяет человекочитаемые имена для модели в единственном и
        множественном числе, а также порядок сортировки по умолчанию.
        """

        verbose_name = "Пользователь"
        verbose_name_plural = "Пользователи"
        ordering = ["email"]
