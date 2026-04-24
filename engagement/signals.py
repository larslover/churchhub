from django.db.models.signals import post_save
from django.dispatch import receiver
from django.contrib.auth import get_user_model

from .models import Group, GroupMember

User = get_user_model()

@receiver(post_save, sender=Group)
def add_default_members_to_group(sender, instance, created, **kwargs):
    if not created:
        return

    if instance.leader:
        GroupMember.objects.get_or_create(
            user=instance.leader,
            group=instance
        )