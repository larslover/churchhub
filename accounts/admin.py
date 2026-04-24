from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import User


@admin.register(User)
class CustomUserAdmin(UserAdmin):
    model = User

    list_display = ("phone", "full_name", "email", "role", "is_staff")
    ordering = ("phone",)

    fieldsets = (
        (None, {"fields": ("phone", "password")}),
        ("Personal Info", {"fields": ("full_name", "email")}),
        ("Permissions", {
            "fields": (
                "is_active",
                "is_staff",
                "is_superuser",
                "groups",
                "user_permissions",
            )
        }),
        ("Church Role", {"fields": ("role",)}),
        ("Important Dates", {"fields": ("last_login", "date_joined")}),
    )

    add_fieldsets = (
        (None, {
            "classes": ("wide",),
            "fields": (
                "phone",
                "full_name",
                "email",
                "password1",
                "password2",
                "role",
                "is_staff",
                "is_superuser",
            ),
        }),
    )

    search_fields = ("phone", "full_name", "email")