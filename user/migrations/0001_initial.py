# Generated by Django 5.2.3 on 2025-06-20 05:22

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ("auth", "0012_alter_user_first_name_max_length"),
    ]

    operations = [
        migrations.CreateModel(
            name="User",
            fields=[
                ("id", models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID")),
                ("password", models.CharField(max_length=128, verbose_name="password")),
                (
                    "email",
                    models.EmailField(
                        error_messages={"unique": "Пользователь с таким email уже существует."},
                        help_text="Укажите адрес электронной почты",
                        max_length=254,
                        unique=True,
                        verbose_name="Email",
                    ),
                ),
                (
                    "phone",
                    models.CharField(
                        blank=True, help_text="Укажите номер телефона", max_length=20, verbose_name="Номер телефона"
                    ),
                ),
                (
                    "first_name",
                    models.CharField(blank=True, help_text="Укажите имя", max_length=30, verbose_name="Имя"),
                ),
                (
                    "last_name",
                    models.CharField(blank=True, help_text="Укажите фамилию", max_length=30, verbose_name="Фамилия"),
                ),
                (
                    "image",
                    models.ImageField(
                        blank=True,
                        help_text="Загрузите аватар",
                        null=True,
                        upload_to="avatars/",
                        verbose_name="Аватар",
                    ),
                ),
                (
                    "role",
                    models.CharField(
                        blank=True,
                        choices=[("user", "Пользователь"), ("admin", "Администратор")],
                        default="user",
                        help_text="Укажите вашу роль",
                        max_length=20,
                        verbose_name="Роль",
                    ),
                ),
                ("is_active", models.BooleanField(default=True, verbose_name="Активен")),
                ("is_staff", models.BooleanField(default=False, verbose_name="Сотрудник")),
                ("is_superuser", models.BooleanField(default=False, verbose_name="Суперпользователь")),
                ("last_login", models.DateTimeField(auto_now=True, verbose_name="Последний вход")),
                ("date_joined", models.DateTimeField(auto_now_add=True, verbose_name="Дата регистрации")),
                (
                    "groups",
                    models.ManyToManyField(
                        blank=True,
                        help_text="The groups this user belongs to. A user will get all permissions granted to each of their groups.",
                        related_name="user_set",
                        related_query_name="user",
                        to="auth.group",
                        verbose_name="groups",
                    ),
                ),
                (
                    "user_permissions",
                    models.ManyToManyField(
                        blank=True,
                        help_text="Specific permissions for this user.",
                        related_name="user_set",
                        related_query_name="user",
                        to="auth.permission",
                        verbose_name="user permissions",
                    ),
                ),
            ],
            options={
                "verbose_name": "Пользователь",
                "verbose_name_plural": "Пользователи",
                "ordering": ["email"],
            },
        ),
    ]
