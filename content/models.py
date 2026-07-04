from django.db import models
from django.utils.text import slugify


# ===============================
# BIBLE BOOKS
# ===============================

class BibleBook(models.Model):

    TESTAMENT_CHOICES = [
        ("OT", "Old Testament"),
        ("NT", "New Testament"),
    ]

    name = models.CharField(max_length=100, unique=True)

    testament = models.CharField(
        max_length=2,
        choices=TESTAMENT_CHOICES
    )

    order = models.PositiveIntegerField()

    class Meta:
        ordering = ["order"]

    def __str__(self):
        return self.name


# ===============================
# TOPICS
# ===============================

class Topic(models.Model):

    name = models.CharField(max_length=100, unique=True)
    slug = models.SlugField(unique=True, blank=True)
    description = models.TextField(blank=True)

    class Meta:
        ordering = ["name"]

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)

        super().save(*args, **kwargs)

    def __str__(self):
        return self.name


# ===============================
# SERIES
# ===============================

class Series(models.Model):

    title = models.CharField(max_length=200)
    slug = models.SlugField(unique=True, blank=True)
    description = models.TextField(blank=True)

    class Meta:
        verbose_name_plural = "Series"
        ordering = ["title"]

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.title)

        super().save(*args, **kwargs)

    def __str__(self):
        return self.title


# ===============================
# TAGS
# ===============================

class Tag(models.Model):

    name = models.CharField(max_length=50, unique=True)

    class Meta:
        ordering = ["name"]

    def __str__(self):
        return self.name


# ===============================
# TEACHINGS
# ===============================

class Teaching(models.Model):

    title = models.CharField(max_length=255)
    slug = models.SlugField(unique=True, blank=True)

    summary = models.TextField(blank=True)

    content = models.TextField()

    topic = models.ForeignKey(
        Topic,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="teachings"
    )

    series = models.ForeignKey(
        Series,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="teachings"
    )

    bible_book = models.ForeignKey(
        BibleBook,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="teachings"
    )

    tags = models.ManyToManyField(
        Tag,
        blank=True,
        related_name="teachings"
    )

    scripture_reference = models.CharField(
        max_length=255,
        blank=True,
        help_text="Example: Romans 8, John 3:16"
    )

    featured_image = models.ImageField(
        upload_to="teachings/",
        blank=True,
        null=True
    )

    is_published = models.BooleanField(default=True)

    published_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ["-published_at"]

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.title)

        super().save(*args, **kwargs)

    def __str__(self):
        return self.title


# ===============================
# RESOURCES
# ===============================

class Resource(models.Model):

    teaching = models.ForeignKey(
        Teaching,
        on_delete=models.CASCADE,
        related_name="resources"
    )

    title = models.CharField(max_length=255)

    pdf = models.FileField(
        upload_to="resources/",
        blank=True,
        null=True
    )

    audio_url = models.URLField(blank=True)
    video_url = models.URLField(blank=True)

    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title