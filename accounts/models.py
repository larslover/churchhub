from django.contrib.auth.models import AbstractUser, BaseUserManager
from django.db import models
from phonenumber_field.modelfields import PhoneNumberField


# ===============================
# 👤 USER MANAGER
# ===============================
class UserManager(BaseUserManager):
    def create_user(self, phone, password=None, **extra_fields):
        if not phone:
            raise ValueError("Phone number is required")

        user = self.model(phone=phone, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, phone, password=None, **extra_fields):
        extra_fields.setdefault("is_staff", True)
        extra_fields.setdefault("is_superuser", True)
        extra_fields.setdefault("is_active", True)

        if extra_fields.get("is_staff") is not True:
            raise ValueError("Superuser must have is_staff=True.")

        if extra_fields.get("is_superuser") is not True:
            raise ValueError("Superuser must have is_superuser=True.")

        return self.create_user(phone, password, **extra_fields)


# ===============================
# 👤 USER MODEL (GLOBAL IDENTITY)
# ===============================
class User(AbstractUser):
    username = None
    first_name = None
    last_name = None

    full_name = models.CharField(max_length=255)

    phone = PhoneNumberField(
        unique=True,
        help_text="Use country code, e.g. +919876543210"
    )

    email = models.EmailField(
        unique=True,
        blank=True,
        null=True
    )

    is_verified = models.BooleanField(default=False)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    USERNAME_FIELD = "phone"
    REQUIRED_FIELDS = ["full_name"]

    objects = UserManager()

    def __str__(self):
        return self.full_name or str(self.phone)

# ===============================
# 🏢 ORGANIZATION (TENANT)
# ===============================
import uuid
from django.db import models
from django.utils.text import slugify


class Organization(models.Model):
    name = models.CharField(max_length=255)

    slug = models.SlugField(
        unique=True,
        blank=True
    )

    join_code = models.CharField(
        max_length=12,
        unique=True,
        blank=True
    )

    # =========================
    # 🎨 BRANDING
    # =========================
    display_name = models.CharField(
        max_length=255,
        blank=True,
        null=True
    )

    logo = models.ImageField(
        upload_to="org_logos/",
        blank=True,
        null=True
    )

    primary_color = models.CharField(
        max_length=20,
        blank=True,
        null=True,
        help_text="Hex color like #0d6efd"
    )

    is_active = models.BooleanField(default=False)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    # ===============================
    # 🔑 GENERATE JOIN CODE
    # ===============================
    def generate_join_code(self):
        words = self.name.split()

        if len(words) >= 2:
            base = "".join(word[0] for word in words[:3]).upper()
        else:
            base = self.name.replace(" ", "").upper()[:6]

        while True:
            code = f"{base}{uuid.uuid4().hex[:4].upper()}"

            if not Organization.objects.filter(join_code=code).exclude(pk=self.pk).exists():
                return code

    # ===============================
    # 💾 SAVE
    # ===============================
    def save(self, *args, **kwargs):

        # slug auto create
        if not self.slug:
            base_slug = slugify(self.name)
            slug = base_slug
            counter = 1

            while Organization.objects.filter(slug=slug).exclude(pk=self.pk).exists():
                slug = f"{base_slug}-{counter}"
                counter += 1

            self.slug = slug

        # join code
        if not self.join_code:
            self.join_code = self.generate_join_code()

        # branding fallback
        if not self.display_name:
            self.display_name = self.name

        # default color
        if not self.primary_color:
            self.primary_color = "#198754"

        super().save(*args, **kwargs)

    # ===============================
    # DISPLAY
    # ===============================
    def __str__(self):
        return self.display_name or self.name# ===============================
# 🔗 ORGANIZATION MEMBERSHIP
# ===============================
class OrganizationMember(models.Model):
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name="memberships"
    )

    organization = models.ForeignKey(
        Organization,
        on_delete=models.CASCADE,
        related_name="members"
    )

    is_admin = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)

    joined_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ("user", "organization")

    def __str__(self):
        return f"{self.user} → {self.organization}"
    
class OrganizationJoinRequest(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    organization = models.ForeignKey(Organization, on_delete=models.CASCADE)

    approved = models.BooleanField(default=False)
    rejected = models.BooleanField(default=False)

    reviewed_by = models.ForeignKey(
        User,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="reviewed_org_requests"
    )

    created_at = models.DateTimeField(auto_now_add=True)
    reviewed_at = models.DateTimeField(null=True, blank=True)

    class Meta:
        unique_together = ("user", "organization")