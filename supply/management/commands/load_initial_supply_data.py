# supply/management/commands/load_initial_supply_data.py
from django.core.management import call_command
from django.core.management.base import BaseCommand

from supply.models import Node, Product


class Command(BaseCommand):
    help = "Загружает фикстуры узлов сети и продуктов в базу данных"

    def handle(self, *args, **kwargs):
        if Node.objects.count() == 0:
            self.stdout.write("Loading node fixture...")
            call_command("loaddata", "supply/fixtures/nodes.json", verbosity=2)
            self.stdout.write("Node fixture successfully loaded...")
        else:
            self.stdout.write("Node fixture already loaded.")

        if Product.objects.count() == 0:
            self.stdout.write("Loading product fixture...")
            call_command("loaddata", "supply/fixtures/products.json", verbosity=2)
            self.stdout.write("Product fixture successfully loaded...")
        else:
            self.stdout.write("Product fixture already loaded.")
