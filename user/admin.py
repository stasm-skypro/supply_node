from django.contrib import admin

from supply.models import Node, Product


@admin.register(Node)
class NodeAdmin(admin.ModelAdmin):
    list_display = (
        "name",
        "email",
        "phone",
        "country",
        "city",
        "street",
        "building_number",
        "supplier",
        "debt_to_supplier",
        "created_at",
    )
    list_filter = ("city",)
    search_fields = ("name", "email", "phone")


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ("name", "model", "release_date", "owner")
    list_filter = ("name",)
    search_fields = ("name", "model")
