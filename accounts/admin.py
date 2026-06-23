from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import User


# ===============================
# 👤 USER ADMIN
# ===============================
@admin.register(User)
class CustomUserAdmin(UserAdmin):
    model = User

    list_display = (
        "email",
        "full_name",
        "is_staff",
        "is_verified",
    )

    ordering = ("email",)

    fieldsets = (
        (None, {
            "fields": (
                "email",
                "password",
            )
        }),

        ("Personal Info", {
            "fields": (
                "full_name",
                "is_verified",
            )
        }),

        ("Permissions", {
            "fields": (
                "is_active",
                "is_staff",
                "is_superuser",
                "groups",
                "user_permissions",
            )
        }),

        ("Important Dates", {
            "fields": (
                "last_login",
                "date_joined",
            )
        }),
    )

    add_fieldsets = (
        (None, {
            "classes": ("wide",),
            "fields": (
                "email",
                "full_name",
                "password1",
                "password2",
                "is_staff",
                "is_superuser",
                "is_active",
            ),
        }),
    )

    search_fields = (
        "email",
        "full_name",
    )