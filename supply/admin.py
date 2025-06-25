import logging
from decimal import Decimal

from django.contrib import admin
from django.urls import reverse
from django.utils.safestring import mark_safe

from supply.models import Node, Product

logger = logging.getLogger(__name__)


@admin.action(description="Очистить задолженность перед поставщиком")
def clear_debt(modeladmin, request, queryset):
    updated = queryset.update(debt_to_supplier=Decimal("0.00"))

    logger.info(
        f"Админ-действие: Администратор сети {request.user} очистил задолженность "
        f"у {updated} объектов Node. ID: {[obj.id for obj in queryset]}"
    )


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
    list_filter = (
        "country",
        "city",
    )
    search_fields = ("name", "email", "phone")
    actions = [clear_debt]


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ("name", "model", "release_date", "owner")
    list_filter = ("name",)
    search_fields = ("name", "model")
