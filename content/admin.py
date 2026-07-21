from django.contrib import admin
# Added BibleBook to the imports
from .models import Topic, Series, Tag, Teaching, Resource, Church, BibleBook


@admin.register(Church)
class ChurchAdmin(admin.ModelAdmin):
    list_display = ("city", "country", "is_active")
    list_filter = ("country", "is_active")
    search_fields = ("city", "country")


# NEW: Register BibleBook so you can manage books in the admin panel
@admin.register(BibleBook)
class BibleBookAdmin(admin.ModelAdmin):
    list_display = ("name", "testament", "order")
    list_filter = ("testament",)
    search_fields = ("name",)


@admin.register(Teaching)
class TeachingAdmin(admin.ModelAdmin):
    list_display = (
        "title",
        "topic",
        "series",
        "is_published",
        "published_at",
    )

    # Added "bible_book" here so you can filter teachings by book
    list_filter = (
        "is_published",
        "topic",
        "series",
        "bible_book", 
    )

    search_fields = (
        "title",
        "summary",
        "content",
    )

    prepopulated_fields = {
        "slug": ("title",)
    }


# Cleaned up the registration syntax error from your original file
admin.site.register(Topic)

admin.site.register(Tag)

