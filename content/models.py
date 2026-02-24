from django.db import models


# content/models.py

class Program(models.Model):
    title = models.CharField(max_length=200)
    description = models.TextField()
    image = models.ImageField(upload_to="programs/", blank=True, null=True)
    day = models.CharField(max_length=100, blank=True)
    time = models.CharField(max_length=100, blank=True)
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return self.title

class Update(models.Model):
    title = models.CharField(max_length=255)
    body = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    # Optional publishing control (useful later)
    is_published = models.BooleanField(default=True)

    def __str__(self):
        return self.title

    class Meta:
        ordering = ["-created_at"]  # newest first

  # content/models.py
from django.db import models
from django.utils.html import mark_safe

class Media(models.Model):
    MEDIA_TYPES = [
        ("video", "Video"),
        ("audio", "Audio"),
    ]
    title = models.CharField(max_length=200)
    media_type = models.CharField(max_length=10, choices=MEDIA_TYPES)
    
    # Either a URL for YouTube/video or a local upload
    media_url = models.URLField(blank=True, null=True)
    upload_file = models.FileField(upload_to="media/", blank=True, null=True)
    
    # Optional thumbnail for preview (for videos or audios)
    image = models.ImageField(upload_to="programs/", blank=True, null=True)
    
    is_published = models.BooleanField(default=True)

    def __str__(self):
        return self.title

    @property
    def embed_url(self):
        """Return an iframe-ready URL for YouTube videos."""
        if not self.media_url:
            return None
        if "youtu.be" in self.media_url:
            video_id = self.media_url.split("/")[-1]
            return f"https://www.youtube.com/embed/{video_id}"
        elif "youtube.com" in self.media_url:
            from urllib.parse import urlparse, parse_qs
            query = urlparse(self.media_url).query
            video_id = parse_qs(query).get("v")
            if video_id:
                return f"https://www.youtube.com/embed/{video_id[0]}"
        return self.media_url  # fallback: return original URL

    def thumbnail_preview(self):
        """For Django admin list display."""
        if self.thumbnail:
            return mark_safe(f'<img src="{self.thumbnail.url}" style="width:60px; height:auto;" />')
        return ""
    thumbnail_preview.short_description = "Thumbnail"