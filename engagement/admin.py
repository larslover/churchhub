from django.contrib import admin
from django.contrib.auth import get_user_model
from .models import Group, GroupMember, Meeting, GroupInvitation
from django.db import models
User = get_user_model()


# ===============================
# 👥 GROUP ADMIN
# ===============================
@admin.register(Group)
class GroupAdmin(admin.ModelAdmin):
    list_display = ("name", "leader", "is_active", "created_at")
    list_filter = ("is_active", "created_at")
    search_fields = ("name", "description")

    fields = ("name", "description", "leader", "image", "is_active")

    def get_queryset(self, request):
        qs = super().get_queryset(request)

        if request.user.is_superuser:
            return qs

        # SaaS SAFETY: only show groups where user is leader or member
        return qs.filter(
            models.Q(leader=request.user) |
            models.Q(members__user=request.user)
        ).distinct()

    def save_model(self, request, obj, form, change):
        if not request.user.is_superuser and not obj.leader:
            obj.leader = request.user
        super().save_model(request, obj, form, change)


# ===============================
# 📅 MEETING ADMIN
# ===============================
@admin.register(Meeting)
class MeetingAdmin(admin.ModelAdmin):
    list_display = ("title", "group", "start_time", "location")
    list_filter = ("start_time",)

    def get_queryset(self, request):
        qs = super().get_queryset(request)

        if request.user.is_superuser:
            return qs

        return qs.filter(
            group__leader=request.user
        )

    def formfield_for_foreignkey(self, db_field, request, **kwargs):
        if db_field.name == "group" and not request.user.is_superuser:
            kwargs["queryset"] = Group.objects.filter(leader=request.user)

        return super().formfield_for_foreignkey(db_field, request, **kwargs)


# ===============================
# 👤 GROUP MEMBER ADMIN
# ===============================
@admin.register(GroupMember)
class GroupMemberAdmin(admin.ModelAdmin):
    list_display = ("user", "group", "joined_at", "is_active")
    list_filter = ("is_active",)

    def get_queryset(self, request):
        qs = super().get_queryset(request)

        if request.user.is_superuser:
            return qs

        return qs.filter(group__leader=request.user)


# ===============================
# 📩 GROUP INVITATION ADMIN
# ===============================
@admin.register(GroupInvitation)
class GroupInvitationAdmin(admin.ModelAdmin):
    list_display = ("group", "invited_user", "invited_by", "accepted", "created_at")
    list_filter = ("accepted", "created_at")

    def get_queryset(self, request):
        qs = super().get_queryset(request)

        if request.user.is_superuser:
            return qs

        return qs.filter(group__leader=request.user)

    def formfield_for_foreignkey(self, db_field, request, **kwargs):
        if request.user.is_superuser:
            return super().formfield_for_foreignkey(db_field, request, **kwargs)

        if db_field.name == "group":
            kwargs["queryset"] = Group.objects.filter(leader=request.user)

        if db_field.name == "invited_by":
            kwargs["queryset"] = User.objects.filter(id=request.user.id)

        return super().formfield_for_foreignkey(db_field, request, **kwargs)