from django.db.models.signals import post_save
from django.dispatch import receiver
from django.contrib.auth import get_user_model

from .models import Group, GroupMember

User = get_user_model()

@receiver(post_save, sender=Group)
def add_admin_to_ministrial(sender, instance, created, **kwargs):
    if created and instance.group_type == "ministrial":
        for admin in User.objects.filter(is_superuser=True):
            GroupMember.objects.get_or_create(user=admin, group=instance)