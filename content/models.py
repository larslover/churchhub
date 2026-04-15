from django.db import models
from django.utils.html import format_html
from django.core.exceptions import ValidationError
from PIL import Image
import re


# ===============================
# 🔒 FILE SIZE VALIDATOR
# ===============================
def validate_file_size(file):
    max_size_mb = 2  # 🔥 change limit here

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
        # Fail silently (prevents crashes)
        pass


# ===============================
# 📘 PROGRAM
# ===============================
class Program(models.Model):
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
    title = models.CharField(max_length=255)
    body = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    is_published = models.BooleanField(default=True)

    class Meta:
        ordering = ["-created_at"]

    def __str__(self):
        return self.title


# ===============================
# 🙏 DEVOTIONAL
# ===============================
class Devotional(models.Model):
    title = models.CharField(max_length=255)
    verse_reference = models.CharField(max_length=255, blank=True)
    verse_text = models.TextField(blank=True)
    message = models.TextField()

    date = models.DateField(auto_now_add=True)
    is_active = models.BooleanField(default=True)

    class Meta:
        ordering = ["-date"]

    def save(self, *args, **kwargs):
        if self.is_active:
            Devotional.objects.filter(is_active=True).exclude(id=self.id).update(is_active=False)

        super().save(*args, **kwargs)

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

    title = models.CharField(max_length=200)
    media_type = models.CharField(max_length=10, choices=MEDIA_TYPES)

    # External link (YouTube, etc.)
    media_url = models.URLField(blank=True, null=True)

    # Local file upload
    upload_file = models.FileField(
        upload_to="media/",
        blank=True,
        null=True,
        validators=[validate_file_size]
    )

    # Thumbnail image
    image = models.ImageField(
        upload_to="programs/",
        blank=True,
        null=True,
        validators=[validate_file_size]
    )

    is_published = models.BooleanField(default=True)

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)

        if self.image:
            resize_image(self.image)

    def __str__(self):
        return self.title


    # ===============================
    # 🎥 YOUTUBE ID EXTRACTION
    # ===============================
    def get_youtube_id(self):
        if not self.media_url:
            return None

        regex = r"(?:v=|\/live\/|youtu\.be\/)([A-Za-z0-9_-]{11})"
        match = re.search(regex, self.media_url)
        return match.group(1) if match else None


    # ===============================
    # 🖼 THUMBNAIL URL
    # ===============================
    def get_thumbnail_url(self):
        video_id = self.get_youtube_id()
        if video_id:
            return f"https://img.youtube.com/vi/{video_id}/hqdefault.jpg"
        return None


    # ===============================
    # 👀 ADMIN PREVIEW
    # ===============================
    def thumbnail_preview(self):
        thumbnail = self.get_thumbnail_url()

        if thumbnail:
            return format_html(
                '<img src="{}" style="width:120px; height:auto;" />',
                thumbnail
            )

        if self.image:
            return format_html(
                '<img src="{}" style="width:120px; height:auto;" />',
                self.image.url
            )

        return "No preview"

    thumbnail_preview.short_description = "Thumbnail"