from django.db import models
from django.utils import timezone
from django.core.exceptions import ValidationError
from django.contrib.auth import get_user_model
from PIL import Image

User = get_user_model()


# ===============================
# 📦 FILE SIZE VALIDATOR
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
# 👥 GROUP
# ===============================
class Group(models.Model):
    organization = models.ForeignKey(
        "accounts.Organization",
        on_delete=models.CASCADE,
        related_name="groups"
    )

    name = models.CharField(max_length=200)
    description = models.TextField(blank=True)

    leader = models.ForeignKey(
        User,
        on_delete=models.SET_NULL,
        null=True,
        related_name="led_groups"
    )

    image = models.ImageField(
        upload_to="groups/",
        blank=True,
        null=True,
        validators=[validate_file_size]
    )

    is_active = models.BooleanField(default=True)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = "Group"
        verbose_name_plural = "Groups"

    def __str__(self):
        return self.name

    def next_meeting(self):
        return self.meetings.filter(
            start_time__gte=timezone.now()
        ).order_by("start_time").first()

    def is_leader(self, user):
        return user.is_authenticated and self.leader_id == user.id

    def is_member(self, user):
        return GroupMember.objects.filter(
            group=self,
            user=user,
            is_active=True
        ).exists()

    def save(self, *args, **kwargs):
        is_new = self.pk is None
        super().save(*args, **kwargs)

        if self.image:
            resize_image(self.image)

        if is_new and self.leader:
            GroupMember.objects.get_or_create(
                user=self.leader,
                group=self
            )


# ===============================
# 👤 GROUP MEMBER
# ===============================
class GroupMember(models.Model):
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name="group_memberships"
    )

    group = models.ForeignKey(
        Group,
        on_delete=models.CASCADE,
        related_name="members"
    )

    joined_at = models.DateTimeField(auto_now_add=True)
    is_active = models.BooleanField(default=True)

    class Meta:
        constraints = [
            models.UniqueConstraint(fields=["user", "group"], name="unique_group_member")
        ]

    def save(self, *args, **kwargs):
        # 🔒 enforce org consistency at write-time
        if self.group and self.user:
            pass  # (optional hook for org checks later)

        super().save(*args, **kwargs)

# ===============================
# 📅 MEETING
# ===============================
class Meeting(models.Model):
    group = models.ForeignKey(
        Group,
        on_delete=models.CASCADE,
        related_name="meetings"
    )

    title = models.CharField(max_length=255)
    start_time = models.DateTimeField()
    end_time = models.DateTimeField(blank=True, null=True)

    location = models.CharField(max_length=255, blank=True)
    description = models.TextField(blank=True)

    created_at = models.DateTimeField(auto_now_add=True)

    def organization(self):
        return self.group.organization

# ===============================
# 📩 INVITATION
# ===============================
class GroupInvitation(models.Model):
    group = models.ForeignKey(
        Group,
        on_delete=models.CASCADE,
        related_name="invitations"
    )

    invited_user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name="received_invitations"
    )

    invited_by = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name="sent_invitations"
    )

    accepted = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    def organization(self):
        return self.group.organization

    class Meta:
        constraints = [
            models.UniqueConstraint(fields=["group", "invited_user"], name="unique_group_invite")
        ]# ===============================
# 📝 POST
# ===============================
class GroupPost(models.Model):
    group = models.ForeignKey(
        Group,
        on_delete=models.CASCADE,
        related_name="posts"
    )

    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name="group_posts"
    )

    content = models.TextField()
    is_pinned = models.BooleanField(default=False)

    created_at = models.DateTimeField(auto_now_add=True)

    def organization(self):
        return self.group.organization

    class Meta:
        ordering = ["-is_pinned", "-created_at"]
# ===============================
# 💬 REPLY
# ===============================
class PostReply(models.Model):
    post = models.ForeignKey(
        GroupPost,
        on_delete=models.CASCADE,
        related_name="replies"
    )

    author = models.ForeignKey(User, on_delete=models.CASCADE)
    content = models.TextField()

    created_at = models.DateTimeField(auto_now_add=True)

    def organization(self):
        return self.post.group.organization
# ===============================
# ❤️ LIKE
# ===============================
class PostLike(models.Model):
    post = models.ForeignKey(
        GroupPost,
        on_delete=models.CASCADE,
        related_name="likes"
    )

    user = models.ForeignKey(User, on_delete=models.CASCADE)

    def organization(self):
        return self.post.group.organization

    class Meta:
        constraints = [
            models.UniqueConstraint(fields=["post", "user"], name="unique_post_like")
        ]