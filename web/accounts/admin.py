"""
Admin configuration for accounts app.
"""
from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import CustomUser, UserProfile


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
