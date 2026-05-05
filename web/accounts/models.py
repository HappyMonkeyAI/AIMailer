"""
Custom User model for AIMailer.
"""
import base64
from django.conf import settings
from cryptography.fernet import Fernet
from django.contrib.auth.models import AbstractUser, BaseUserManager
from django.db import models
from django.utils.translation import gettext_lazy as _


class CustomUserManager(BaseUserManager):
    """
    Custom user model manager where email is the unique identifier
    for authentication instead of usernames.
    """
    def create_user(self, email, password=None, **extra_fields):
        if not email:
            raise ValueError(_('The Email must be set'))
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save()
        return user

    def create_superuser(self, email, password, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        extra_fields.setdefault('is_active', True)

        if extra_fields.get('is_staff') is not True:
            raise ValueError(_('Superuser must have is_staff=True.'))
        if extra_fields.get('is_superuser') is not True:
            raise ValueError(_('Superuser must have is_superuser=True.'))
        return self.create_user(email, password, **extra_fields)


class CustomUser(AbstractUser):
    """
    Custom user model with email as the primary identifier.
    """
    SUBSCRIPTION_TIERS = [
        ('free', 'Free'),
        ('pro', 'Pro'),
        ('enterprise', 'Enterprise'),
    ]
    
    email = models.EmailField(_('email address'), unique=True)
    email_verified = models.BooleanField(default=False)
    subscription_tier = models.CharField(
        max_length=20,
        choices=SUBSCRIPTION_TIERS,
        default='free'
    )
    two_factor_enabled = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    objects = CustomUserManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []
    
    class Meta:
        verbose_name = _('user')
        verbose_name_plural = _('users')
    
    def __str__(self):
        return self.email


class UserProfile(models.Model):
    """
    Extended user profile information.
    """
    user = models.OneToOneField(
        CustomUser,
        on_delete=models.CASCADE,
        related_name='profile'
    )
    company_name = models.CharField(max_length=255, blank=True)
    bio = models.TextField(blank=True)
    avatar = models.ImageField(upload_to='avatars/', blank=True, null=True)
    timezone = models.CharField(max_length=50, default='UTC')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return f"Profile for {self.user.email}"


class SMTPConfig(models.Model):
    """
    Custom SMTP configuration for user-specific email sending.
    """
    user = models.OneToOneField(
        CustomUser,
        on_delete=models.CASCADE,
        related_name='smtp_config'
    )
    smtp_host = models.CharField(max_length=255)
    smtp_port = models.IntegerField(default=587)
    smtp_username = models.CharField(max_length=255, blank=True)
    smtp_password = models.CharField(max_length=255, blank=True)
    use_tls = models.BooleanField(default=True)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    def _get_fernet(self):
        # Use SECRET_KEY to derive a 32-byte key for Fernet
        key = base64.urlsafe_b64encode(settings.SECRET_KEY[:32].encode().ljust(32))
        return Fernet(key)

    def save(self, *args, **kwargs):
        if self.smtp_password and not self.smtp_password.startswith('fnc:'):
            f = self._get_fernet()
            self.smtp_password = 'fnc:' + f.encrypt(self.smtp_password.encode()).decode()
        super().save(*args, **kwargs)

    def get_decrypted_password(self):
        if not self.smtp_password:
            return ''
        if not self.smtp_password.startswith('fnc:'):
            return self.smtp_password
        try:
            f = self._get_fernet()
            return f.decrypt(self.smtp_password[4:].encode()).decode()
        except Exception:
            return ''

    class Meta:
        verbose_name = _('SMTP Config')
        verbose_name_plural = _('SMTP Configs')
        
    def __str__(self):
        return f"SMTP Config for {self.user.email}"
