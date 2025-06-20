from decimal import Decimal

from django.contrib import admin
from django.urls import reverse
from django.utils.safestring import mark_safe

from supply.models import Node, Product


@admin.action(description="Очистить задолженность перед поставщиком")
def clear_debt(modeladmin, request, queryset):
    queryset.update(debt_to_supplier=Decimal("0.00"))


@admin.register(Node)
class NodeAdmin(admin.ModelAdmin):

    @admin.display(description="Поставщик")
    def supplier_link(self, obj):
        if obj.supplier:
            url = reverse("admin:supply_change", args=[obj.supplier.id])
            return mark_safe(f'<a href="{url}">{obj.supplier.name}</a>')
        return "-"

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
    actions = [clear_debt]


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ("name", "model", "release_date", "owner")
    list_filter = ("name",)
    search_fields = ("name", "model")
