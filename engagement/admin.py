from django.contrib import admin
from .models import Group, GroupMember, Meeting, GroupInvitation

# -------------------------
# Group Admin
# -------------------------
class GroupAdmin(admin.ModelAdmin):
    list_display = ("name", "leader", "group_type", "is_active", "created_at")
    list_filter = ("group_type", "is_active")
    search_fields = ("name", "description")
    fields = ("name", "description", "leader", "group_type", "image", "is_active")  # explicitly show group_type

    def get_readonly_fields(self, request, obj=None):
        if request.user.is_superuser:
            return []
        return ["leader"]

    def save_model(self, request, obj, form, change):
        if not request.user.is_superuser and not obj.leader:
            obj.leader = request.user
        super().save_model(request, obj, form, change)
# -------------------------
# Meeting Admin
# -------------------------
class MeetingAdmin(admin.ModelAdmin):
    list_display = ("title", "group", "start_time", "location")
    list_filter = ("group",)

    def get_queryset(self, request):
        qs = super().get_queryset(request)
        if request.user.is_superuser:
            return qs
        return qs.filter(group__leader=request.user)

    def formfield_for_foreignkey(self, db_field, request, **kwargs):
        if db_field.name == "group" and not request.user.is_superuser:
            kwargs["queryset"] = Group.objects.filter(leader=request.user)
        return super().formfield_for_foreignkey(db_field, request, **kwargs)


# -------------------------
# GroupMember Admin
# -------------------------
class GroupMemberAdmin(admin.ModelAdmin):
    list_display = ("user", "group", "joined_at", "is_active")
    list_filter = ("group", "is_active")

    def get_queryset(self, request):
        qs = super().get_queryset(request)
        if request.user.is_superuser:
            return qs
        return qs.filter(group__leader=request.user)


# -------------------------
# GroupInvitation Admin
# -------------------------
class GroupInvitationAdmin(admin.ModelAdmin):
    list_display = ("group", "invited_user", "invited_by", "accepted", "created_at")
    list_filter = ("group", "accepted")

    def get_queryset(self, request):
        qs = super().get_queryset(request)
        if request.user.is_superuser:
            return qs
        # Only show invitations for groups this user leads
        return qs.filter(group__leader=request.user)

    def formfield_for_foreignkey(self, db_field, request, **kwargs):
        if db_field.name == "group" and not request.user.is_superuser:
            kwargs["queryset"] = Group.objects.filter(leader=request.user)
        if db_field.name == "invited_by" and not request.user.is_superuser:
            kwargs["queryset"] = User.objects.filter(id=request.user.id)
        return super().formfield_for_foreignkey(db_field, request, **kwargs)


# Register models
admin.site.register(Group, GroupAdmin)
admin.site.register(Meeting, MeetingAdmin)
admin.site.register(GroupMember, GroupMemberAdmin)
admin.site.register(GroupInvitation, GroupInvitationAdmin)