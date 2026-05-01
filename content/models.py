from django.db import models
from django.utils.html import format_html
from django.core.exceptions import ValidationError
from PIL import Image
import re


# ===============================
# 🔒 FILE SIZE VALIDATOR
# ===============================
def validate_file_size(file):
    max_size_mb = 2

    if file.size > max_size_mb * 1024 * 1024:
        raise ValidationError(f"File must be under {max_size_mb}MB")


# ===============================
# 🖼 IMAGE RESIZER
# ===============================
def resize_image(image_field, max_width=800, max_height=800):
    try:
        if not image_field:
            return

        img = Image.open(image_field.path)

        if img.height > max_height or img.width > max_width:
            img.thumbnail((max_width, max_height))
            img.save(image_field.path, optimize=True, quality=70)

    except Exception:
        pass


# ===============================
# 📘 PROGRAM
# ===============================
class Program(models.Model):
    organization = models.ForeignKey(
        "accounts.Organization",
        on_delete=models.CASCADE,
        related_name="programs"
    )

    title = models.CharField(max_length=200)
    description = models.TextField()

    image = models.ImageField(
        upload_to="programs/",
        blank=True,
        null=True,
        validators=[validate_file_size]
    )

    day = models.CharField(max_length=100, blank=True)
    time = models.CharField(max_length=100, blank=True)

    is_active = models.BooleanField(default=True)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)

        if self.image:
            resize_image(self.image)

    def __str__(self):
        return self.title


# ===============================
# 📰 UPDATES
# ===============================
class Update(models.Model):
    organization = models.ForeignKey(
        "accounts.Organization",
        on_delete=models.CASCADE,
        related_name="updates"
    )

    title = models.CharField(max_length=255)
    body = models.TextField()

    image = models.ImageField(
        upload_to="updates/",
        blank=True,
        null=True,
        validators=[validate_file_size]
    )

    is_published = models.BooleanField(default=True)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ["-created_at"]

    def __str__(self):
        return self.title

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)

        if self.image:
            resize_image(self.image)


# ===============================
# 🙏 DEVOTIONAL
# ===============================
class Devotional(models.Model):
    organization = models.ForeignKey(
        "accounts.Organization",
        on_delete=models.CASCADE,
        related_name="devotionals"
    )

    title = models.CharField(max_length=255)
    verse_reference = models.CharField(max_length=255, blank=True)
    verse_text = models.TextField(blank=True)
    message = models.TextField()

    date = models.DateField(auto_now_add=True)
    is_active = models.BooleanField(default=True)

    class Meta:
        ordering = ["-date"]

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)

        if self.is_active:
            Devotional.objects.filter(
                organization=self.organization,
                is_active=True
            ).exclude(pk=self.pk).update(is_active=False)

    def __str__(self):
        return f"{self.title} - {self.date}"


# ===============================
# 🎵 MEDIA
# ===============================
class Media(models.Model):
    MEDIA_TYPES = [
        ("video", "Video"),
        ("audio", "Audio"),
    ]

    organization = models.ForeignKey(
        "accounts.Organization",
        on_delete=models.CASCADE,
        related_name="media"
    )

    title = models.CharField(max_length=200)

    media_type = models.CharField(
        max_length=10,
        choices=MEDIA_TYPES,
        default="video"
    )

    # Only external URLs (YouTube / Spotify etc)
    media_url = models.URLField(
        blank=True,
        null=True
    )

    # Keep field optional, but do NOT use uploads
    upload_file = models.FileField(
        upload_to="media/",
        blank=True,
        null=True
    )

    image = models.ImageField(
        upload_to="media/",
        blank=True,
        null=True,
        validators=[validate_file_size]
    )

    is_published = models.BooleanField(default=True)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    # ==================================
    # SAVE
    # ==================================
    def save(self, *args, **kwargs):

        # Prevent file uploads eating server storage
        self.upload_file = None

        super().save(*args, **kwargs)

        if self.image:
            resize_image(self.image)

    def __str__(self):
        return self.title

    # ==================================
    # YOUTUBE ID EXTRACTION
    # ==================================
    def get_youtube_id(self):
        if not self.media_url:
            return None

        url = self.media_url.strip()

        patterns = [
            r"(?:https?:\/\/)?(?:www\.)?youtube\.com\/watch\?v=([A-Za-z0-9_-]{11})",
            r"(?:https?:\/\/)?(?:www\.)?youtu\.be\/([A-Za-z0-9_-]{11})",
            r"(?:https?:\/\/)?(?:www\.)?youtube\.com\/embed\/([A-Za-z0-9_-]{11})",
            r"(?:https?:\/\/)?(?:www\.)?youtube\.com\/shorts\/([A-Za-z0-9_-]{11})",
            r"(?:https?:\/\/)?(?:www\.)?youtube\.com\/live\/([A-Za-z0-9_-]{11})",
        ]

        for pattern in patterns:
            match = re.search(pattern, url)
            if match:
                return match.group(1)

        return None

    # ==================================
    # EMBED URL
    # ==================================
    @property
    def embed_url(self):
        video_id = self.get_youtube_id()
        if video_id:
            return (
                f"https://www.youtube-nocookie.com/embed/{video_id}"
                "?rel=0&modestbranding=1&enablejsapi=1"
            )
        return ""

    # ==================================
    # THUMBNAIL
    # ==================================
    def get_thumbnail_url(self):
        video_id = self.get_youtube_id()

        if video_id:
            return f"https://img.youtube.com/vi/{video_id}/hqdefault.jpg"

        return None

    # ==================================
    # ADMIN PREVIEW
    # ==================================
    def thumbnail_preview(self):
        thumbnail = self.get_thumbnail_url()

        if thumbnail:
            return format_html(
                '<img src="{}" style="width:120px;height:auto;border-radius:8px;" />',
                thumbnail
            )

        if self.image:
            return format_html(
                '<img src="{}" style="width:120px;height:auto;border-radius:8px;" />',
                self.image.url
            )

        return "No preview"

    thumbnail_preview.short_description = "Thumbnail"