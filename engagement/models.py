from django.db import models
from django.conf import settings
from django.utils import timezone
from django.core.exceptions import ValidationError
from django.contrib.auth import get_user_model
from PIL import Image

User = get_user_model()


# ===============================
# 📦 FILE SIZE VALIDATOR
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
        pass


# ===============================
# 👥 GROUP MODEL
# ===============================
class Group(models.Model):

    GROUP_TYPES = [
        ("small", "Small Group"),
        ("ministrial", "Ministrial Group"),
    ]

    name = models.CharField(max_length=200)
    description = models.TextField(blank=True)

    leader = models.ForeignKey(
        User, on_delete=models.SET_NULL, null=True, related_name="led_groups"
    )

    group_type = models.CharField(
        max_length=20, choices=GROUP_TYPES, default="small"
    )

    created_at = models.DateTimeField(auto_now_add=True)
    is_active = models.BooleanField(default=True)

    # ✅ APPLY VALIDATOR HERE
    image = models.ImageField(
        upload_to="groups/",
        blank=True,
        null=True,
        validators=[validate_file_size]
    )

    def __str__(self):
        return self.name

    def next_meeting(self):
        return self.meetings.filter(
            start_time__gte=timezone.now()
        ).order_by('start_time').first()

    # ✅ RESIZE ON SAVE
    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)

        if self.image:
            resize_image(self.image)

    class Meta:
        verbose_name = "Church Group"
        verbose_name_plural = "Church Groups"


# ===============================
# 👤 GROUP MEMBERS
# ===============================
class GroupMember(models.Model):

    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="group_memberships")
    group = models.ForeignKey(Group, on_delete=models.CASCADE, related_name="members")

    joined_at = models.DateTimeField(auto_now_add=True)
    is_active = models.BooleanField(default=True)

    class Meta:
        unique_together = ("user", "group")

    def __str__(self):
        return f"{self.user} in {self.group}"


# ===============================
# 📅 MEETINGS
# ===============================
class Meeting(models.Model):

    group = models.ForeignKey(Group, on_delete=models.CASCADE, related_name="meetings")

    title = models.CharField(max_length=255)
    start_time = models.DateTimeField()
    end_time = models.DateTimeField(blank=True, null=True)

    location = models.CharField(max_length=255, blank=True)
    description = models.TextField(blank=True)

    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["start_time"]

    def __str__(self):
        return f"{self.title} ({self.group.name})"


# ===============================
# 📩 INVITATIONS
# ===============================
class GroupInvitation(models.Model):

    group = models.ForeignKey(Group, on_delete=models.CASCADE, related_name="invitations")
    invited_user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="received_invitations")
    invited_by = models.ForeignKey(User, on_delete=models.CASCADE, related_name="sent_invitations")

    accepted = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ("group", "invited_user")

    def __str__(self):
        status = "Accepted" if self.accepted else "Pending"
        return f"Invite: {self.invited_user} to {self.group} ({status})"

    @property
    def is_pending(self):
        return not self.accepted


# ===============================
# 📝 POSTS
# ===============================
class GroupPost(models.Model):

    group = models.ForeignKey(Group, on_delete=models.CASCADE, related_name='posts')
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name='group_posts')

    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-created_at']


# ===============================
# 💬 REPLIES
# ===============================
class PostReply(models.Model):

    post = models.ForeignKey(GroupPost, on_delete=models.CASCADE, related_name='replies')
    author = models.ForeignKey(User, on_delete=models.CASCADE)

    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)


# ===============================
# ❤️ LIKES
# ===============================
class PostLike(models.Model):

    post = models.ForeignKey(GroupPost, on_delete=models.CASCADE, related_name='likes')
    user = models.ForeignKey(User, on_delete=models.CASCADE)

    class Meta:
        unique_together = ('post', 'user')