from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin, BaseUserManager
from django.db import models
from django.utils import timezone
from django.conf import settings

class UserManager(BaseUserManager):
    def create_user(self, email, password=None):
        if not email:
            raise ValueError("Users must have an email")
        user = self.model(email=email)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password):
        user = self.create_user(
            email=email, password=password
        )
        user.is_active = True
        user.is_staff = True
        user.is_superuser = True
        user.save(using=self._db)
        return user

class UserModel(AbstractBaseUser, PermissionsMixin):
    phone_number = models.CharField(max_length=15, blank=True, null=True)
    email = models.EmailField(max_length=50, unique=True)
    username = models.CharField(max_length=30, default='', blank=False)
    first_name = models.CharField(
        max_length=50, null=False, default='', blank=False)
    last_name = models.CharField(
        max_length=50, null=False, default='', blank=False)
    bio = models.TextField(null=False, default='', blank=False)
    otp = models.CharField(max_length=6)
    otp_attempts = models.IntegerField(default=0)
    last_opt_attempt = models.DateTimeField(blank=True, null=True)
    otp_verified = models.BooleanField(default=False)
    otp_expiry = models.DateTimeField(blank=True, null=True)
    is_active = models.BooleanField(default=False)
    is_staff = models.BooleanField(default=False)
    max_otp_try = models.CharField(max_length=2, default=settings.MAX_OTP_TRY)
    user_registered_at = models.DateTimeField(auto_now_add=True, blank=True)

    # Define unique related_names for the groups and user_permissions fields
    groups = models.ManyToManyField(
        'auth.Group',
        blank=True,
        related_name='usermodel_set',  # Change to a unique name
        related_query_name='usermodel'
    )
    user_permissions = models.ManyToManyField(
        'auth.Permission',
        blank=True,
        related_name='usermodel_set',  # Change to a unique name
        related_query_name='usermodel'
    )

    USERNAME_FIELD = 'email'

    objects = UserManager()

    def __str__(self):
        return self.email

class UserProfile(models.Model):
    user = models.OneToOneField(
        UserModel,
        related_name="profile",
        on_delete=models.CASCADE,
        primary_key=True,
    )


