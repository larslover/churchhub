from django.contrib.auth.models import AbstractUser
from django.db import models

class User(AbstractUser):
    phone = models.CharField(max_length=20, blank=True)

    ROLE_CHOICES = (
        ("member", "Member"),
        ("leader", "Leader"),
        ("pastor", "Pastor"),
        ("admin", "Admin"),
    )
    role = models.CharField(max_length=10, choices=ROLE_CHOICES, default="member")

    def __str__(self):
        return self.get_full_name() or self.username