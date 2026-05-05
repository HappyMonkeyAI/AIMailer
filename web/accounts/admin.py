"""
Admin configuration for accounts app.
"""
from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import CustomUser, UserProfile, SMTPConfig


@admin.register(CustomUser)
class CustomUserAdmin(UserAdmin):
    """
    Custom user admin interface.
    """
    list_display = ['email', 'username', 'subscription_tier', 'email_verified', 'two_factor_enabled', 'is_staff']
    list_filter = ['subscription_tier', 'email_verified', 'two_factor_enabled', 'is_staff', 'is_active']
    search_fields = ['email', 'username', 'first_name', 'last_name']
    ordering = ['-date_joined']
    
    fieldsets = UserAdmin.fieldsets + (
        ('Additional Info', {
            'fields': ('email_verified', 'subscription_tier', 'two_factor_enabled')
        }),
    )


@admin.register(UserProfile)
class UserProfileAdmin(admin.ModelAdmin):
    """
    User profile admin interface.
    """
    list_display = ['user', 'company_name', 'timezone', 'created_at']
    search_fields = ['user__email', 'company_name']
    list_filter = ['timezone']


@admin.register(SMTPConfig)
class SMTPConfigAdmin(admin.ModelAdmin):
    """
    Custom SMTP configuration admin interface.
    """
    list_display = ['user', 'smtp_host', 'smtp_port', 'use_tls', 'is_active', 'password_status', 'updated_at']
    search_fields = ['user__email', 'smtp_host']
    list_filter = ['is_active', 'use_tls']
    
    def password_status(self, obj):
        if obj.smtp_password:
            if obj.smtp_password.startswith('fnc:'):
                return "Encrypted (Secure)"
            return "Plain Text (Unsafe)"
        return "Not Set"
    password_status.short_description = 'Password Status'

    # Password field should be masked in the admin
    def get_form(self, request, obj=None, **kwargs):
        form = super().get_form(request, obj, **kwargs)
        if 'smtp_password' in form.base_fields:
            # Mask the initial value if it's encrypted
            if obj and obj.smtp_password and obj.smtp_password.startswith('fnc:'):
                form.base_fields['smtp_password'].initial = '********'
                form.base_fields['smtp_password'].help_text = 'Encrypted password stored. Enter a new password to update it.'
            form.base_fields['smtp_password'].widget.input_type = 'password'
            form.base_fields['smtp_password'].required = False # Allow saving without changing password
        return form

    def save_model(self, request, obj, form, change):
        # Only update password if it's not the mask
        if form.cleaned_data.get('smtp_password') == '********':
            # Retrieve the original encrypted password from the database
            original_obj = SMTPConfig.objects.get(pk=obj.pk)
            obj.smtp_password = original_obj.smtp_password
        super().save_model(request, obj, form, change)
