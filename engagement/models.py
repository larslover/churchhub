from django.db import models
from django.conf import settings
from django.utils import timezone

User = settings.AUTH_USER_MODEL  # your custom user model

class Group(models.Model):
    """
    Represents a group within the church (e.g., Bible study, youth group, or ministrial groups).
    """
    GROUP_TYPES = [
        ("small", "Small Group"),           # leader invites
        ("ministrial", "Ministrial Group"), # admin appoints
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
    
    image = models.ImageField(upload_to="groups/", blank=True, null=True)

    def __str__(self):
        return self.name

    def next_meeting(self):
        return self.meetings.filter(
            start_time__gte=timezone.now()
        ).order_by('start_time').first()


class GroupMember(models.Model):
    """
    Connects users to groups they belong to.
    """
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="group_memberships")
    group = models.ForeignKey(Group, on_delete=models.CASCADE, related_name="members")
    joined_at = models.DateTimeField(auto_now_add=True)
    is_active = models.BooleanField(default=True)

    class Meta:
        unique_together = ("user", "group")  # user cannot join same group twice

    def __str__(self):
        return f"{self.user} in {self.group}"


class Meeting(models.Model):
    """
    Represents a scheduled meeting for a group.
    """
    group = models.ForeignKey(Group, on_delete=models.CASCADE, related_name="meetings")
    title = models.CharField(max_length=255)
    start_time = models.DateTimeField()
    end_time = models.DateTimeField(blank=True, null=True)
    location = models.CharField(max_length=255, blank=True)
    description = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["start_time"]  # helps next_meeting()

    def __str__(self):
        return f"{self.title} ({self.group.name})"


class GroupInvitation(models.Model):
    """
    Invitation system for small groups: leaders invite members.
    """
    group = models.ForeignKey(Group, on_delete=models.CASCADE, related_name="invitations")
    invited_user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="received_invitations")
    invited_by = models.ForeignKey(User, on_delete=models.CASCADE, related_name="sent_invitations")
    accepted = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ("group", "invited_user")  # prevent duplicate invites

    def __str__(self):
        status = "Accepted" if self.accepted else "Pending"
        return f"Invite: {self.invited_user} to {self.group} ({status})"

    @property
    def is_pending(self):
        return not self.accepted