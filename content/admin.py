from django.contrib import admin

from .models import (
    Topic,
    Series,
    Tag,
    Teaching,
    TeachingAudio,
    Language,
    Resource,
    Church,
    BibleBook,
    ChurchUpdate,
)


# ===============================
# CHURCH
# ===============================

@admin.register(Church)
class ChurchAdmin(admin.ModelAdmin):
    list_display = ("city", "country", "is_active")
    list_filter = ("country", "is_active")
    search_fields = ("city", "country")


# ===============================
# BIBLE BOOK
# ===============================

@admin.register(BibleBook)
class BibleBookAdmin(admin.ModelAdmin):
    list_display = ("name", "testament", "order")
    list_filter = ("testament",)
    search_fields = ("name",)


# ===============================
# LANGUAGE
# ===============================

@admin.register(Language)
class LanguageAdmin(admin.ModelAdmin):
    list_display = ("name", "code")
    search_fields = ("name", "code")


# ===============================
# TEACHING AUDIO INLINE
# ===============================

class TeachingAudioInline(admin.TabularInline):
    model = TeachingAudio
    extra = 1


# ===============================
# TEACHING
# ===============================

@admin.register(Teaching)
class TeachingAdmin(admin.ModelAdmin):

    list_display = (
        "title",
        "topic",
        "series",
        "is_published",
        "published_at",
    )

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

    inlines = [
        TeachingAudioInline,
    ]


# ===============================
# CHURCH UPDATES
# ===============================

@admin.register(ChurchUpdate)
class ChurchUpdateAdmin(admin.ModelAdmin):

    list_display = (
        "title",
        "church",
        "date",
        "is_published",
    )

    list_filter = (
        "church",
        "is_published",
        "date",
    )

    search_fields = (
        "title",
        "summary",
        "content",
    )


# ===============================
# OTHER MODELS
# ===============================

admin.site.register(Topic)
admin.site.register(Tag)
admin.site.register(Resource)