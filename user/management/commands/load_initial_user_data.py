# user/management/commands/load_initial_user_data.py
from django.core.management import call_command
from django.core.management.base import BaseCommand

from user.models import User


class Command(BaseCommand):
    help = "Загружает фикстуры пользователей в базу данных"

    def handle(self, *args, **kwargs):
        if User.objects.count() == 0:
            self.stdout.write("Loading fixtures...")
            call_command("loaddata", "user/fixtures/users.json", verbosity=2)
            self.stdout.write("User fixture successfully loaded...")
        else:
            self.stdout.write("Fixtures already loaded.")
