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


class Media(models.Model):
    MEDIA_TYPES = [
        ("video", "Video"),
        ("audio", "Audio"),
    ]
    title = models.CharField(max_length=200)
    media_type = models.CharField(max_length=10, choices=MEDIA_TYPES)
    
    # Either a URL for YouTube/video or a local upload
    media_url = models.URLField(blank=True, null=True)        # For YouTube links or online videos
    upload_file = models.FileField(upload_to="media/", blank=True, null=True)  # Local files
    
    is_published = models.BooleanField(default=True)

    def __str__(self):
        return self.title