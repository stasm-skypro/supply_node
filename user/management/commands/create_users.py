from django.core.management.base import BaseCommand
from django.utils.timezone import make_aware

from user.models import User


class Command(BaseCommand):
    help = "Создаёт пользователей с захэшированными паролями"

    def handle(self, *args, **options):

        from datetime import datetime

        users_data = [
            {
                "email": "ivanov@example.com",
                "password": "P4$$w0rd",
                "first_name": "Иван",
                "last_name": "Иванов",
                "phone": "+71234567890",
                "role": "user",
                "is_active": True,
                "is_staff": False,
                "is_superuser": False,
                "date_joined": make_aware(datetime(2025, 6, 8, 9, 0, 0)),
                "last_login": make_aware(datetime(2025, 6, 18, 10, 0, 0)),
            },
            {
                "email": "petrova@example.com",
                "password": "P4$$w0rd",
                "first_name": "Ольга",
                "last_name": "Петрова",
                "phone": "+79870001122",
                "role": "user",
                "is_active": False,
                "is_staff": False,
                "is_superuser": False,
                "date_joined": make_aware(datetime(2025, 6, 8, 10, 5, 0)),
                "last_login": make_aware(datetime(2025, 6, 19, 10, 5, 0)),
            },
            {
                "email": "sidorov@example.com",
                "password": "P4$$w0rd",
                "first_name": "Алексей",
                "last_name": "Сидоров",
                "phone": "+79031234567",
                "role": "user",
                "is_active": True,
                "is_staff": False,
                "is_superuser": False,
                "date_joined": make_aware(datetime(2025, 6, 1, 10, 10, 0)),
                "last_login": make_aware(datetime(2025, 6, 20, 10, 10, 0)),
            },
            {
                "email": "kuznetsova@example.com",
                "password": "P4$$w0rd",
                "first_name": "Мария",
                "last_name": "Кузнецова",
                "phone": "+77778889900",
                "role": "user",
                "is_active": True,
                "is_staff": False,
                "is_superuser": False,
                "date_joined": make_aware(datetime(2025, 5, 18, 10, 15, 0)),
                "last_login": make_aware(datetime(2025, 6, 18, 15, 10, 0)),
            },
            {
                "email": "ermek@example.com",
                "password": "P4$$w0rd",
                "first_name": "Ермек",
                "last_name": "Жумабаев",
                "phone": "+77012345678",
                "role": "user",
                "is_active": False,
                "is_staff": False,
                "is_superuser": False,
                "date_joined": make_aware(datetime(2025, 5, 18, 10, 20, 0)),
                "last_login": make_aware(datetime(2025, 6, 19, 10, 20, 0)),
            },
        ]

        for data in users_data:
            if not User.objects.filter(email=data["email"]).exists():
                _ = User.objects.create_user(
                    email=data["email"],
                    password=data["password"],
                    first_name=data["first_name"],
                    last_name=data["last_name"],
                    role=data["role"],
                    is_active=data["is_active"],
                    is_staff=data["is_staff"],
                    is_superuser=data["is_superuser"],
                    date_joined=data["date_joined"],
                    last_login=data["last_login"],
                )
                self.stdout.write(self.style.SUCCESS(f"✅ Пользователь {data['email']} создан"))
            else:
                self.stdout.write(self.style.WARNING(f"⚠️ Пользователь {data['email']} уже существует"))
