from django.contrib import admin
from .models import Media, Program, Update

@admin.register(Media)
class MediaAdmin(admin.ModelAdmin):
    list_display = ("title", "media_type", "is_published")  # only real fields
    list_filter = ("media_type", "is_published")            # only real fields
    search_fields = ("title",)

@admin.register(Program)
class ProgramAdmin(admin.ModelAdmin):
    list_display = ("title", "day", "time", "is_active")  # Program has is_active
    list_filter = ("is_active",)
    search_fields = ("title", "description")

@admin.register(Update)
class UpdateAdmin(admin.ModelAdmin):
    list_display = ("title", "created_at", "is_published")
    list_filter = ("is_published", "created_at")
    search_fields = ("title", "body")