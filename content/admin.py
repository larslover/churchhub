from django.contrib import admin

from django.utils.html import format_html
from .models import Program, Update, Media, Devotional

@admin.register(Devotional)
class DevotionalAdmin(admin.ModelAdmin):
    list_display = (
        "title",
        "verse_reference",
        "date",
        "is_active",
    )

    list_filter = ("is_active", "date")
    search_fields = ("title", "verse_reference", "message")
    ordering = ("-date",)

    fieldsets = (
        ("Content", {
            "fields": (
                "title",
                "verse_reference",
                "verse_text",
                "message",
            )
        }),
        ("Publishing", {
            "fields": (
                "is_active",
            )
        }),
    )

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
from django.contrib import admin
from django.utils.html import format_html
from .models import Update


@admin.register(Update)
class UpdateAdmin(admin.ModelAdmin):
    list_display = (
        "title",
        "created_at",
        "is_published",
        "image_preview",
    )

    list_filter = (
        "is_published",
        "created_at",
    )

    search_fields = (
        "title",
        "body",
    )

    readonly_fields = ("image_preview",)

    fieldsets = (
        ("Content", {
            "fields": (
                "title",
                "body",
            )
        }),
        ("Media", {
            "fields": (
                "image",
                "image_preview",
            )
        }),
        ("Publishing", {
            "fields": (
                "is_published",
            )
        }),
    )

    def image_preview(self, obj):
        if obj.image:
            return format_html(
                '<img src="{}" style="width:160px; height:auto; border-radius:10px;" />',
                obj.image.url
            )
        return "No image"

    image_preview.short_description = "Preview"