from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import User, Organization, OrganizationMember


# ===============================
# 👤 USER ADMIN
# ===============================
@admin.register(User)
class CustomUserAdmin(UserAdmin):
    model = User

    list_display = ("phone", "full_name", "email", "is_staff", "is_verified")
    ordering = ("phone",)

    fieldsets = (
        (None, {"fields": ("phone", "password")}),
        ("Personal Info", {"fields": ("full_name", "email", "is_verified")}),
        ("Permissions", {
            "fields": (
                "is_active",
                "is_staff",
                "is_superuser",
                "groups",
                "user_permissions",
            )
        }),
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
                "is_staff",
                "is_superuser",
                "is_active",
            ),
        }),
    )

    search_fields = ("phone", "full_name", "email")


# ===============================
# 🏢 ORGANIZATION ADMIN
# ===============================
@admin.register(Organization)
class OrganizationAdmin(admin.ModelAdmin):
    list_display = ("name", "slug", "is_active", "created_at")
    search_fields = ("name", "slug")
    prepopulated_fields = {"slug": ("name",)}


# ===============================
# 🔗 MEMBERSHIP ADMIN
# ===============================
@admin.register(OrganizationMember)
class OrganizationMemberAdmin(admin.ModelAdmin):
    list_display = ("user", "organization", "is_admin", "is_active", "joined_at")

    list_filter = ("organization", "is_admin", "is_active")
    search_fields = (
        "user__phone",
        "user__full_name",
        "organization__name",
    )

    autocomplete_fields = ["user", "organization"]