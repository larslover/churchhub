from django.contrib import admin
from .models import Media, Program, Update

from django.contrib import admin
from .models import Media, Program, Update

@admin.register(Media)
class MediaAdmin(admin.ModelAdmin):
    list_display = ("title", "media_type", "is_published", "thumbnail_preview")  # add thumbnail_preview
    list_filter = ("media_type", "is_published")
    search_fields = ("title",)

    readonly_fields = ("thumbnail_preview",)  # if you want the preview in the edit form

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