from django.contrib import admin

from user.models import User


@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    list_display = (
        "email",
        "phone",
        "first_name",
        "last_name",
        "image",
        "role",
        "is_active",
        "is_staff",
        "is_superuser",
    )
    list_filter = (
        "role",
        "email",
    )
    search_fields = ("email",)
