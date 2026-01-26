"""
Admin configuration for newsletters app.
"""
from django.contrib import admin
from .models import Category, Newsletter, NewsletterConfig, RSSSource, Subscriber, SendHistory, EmailEvent


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    """
    Category admin interface.
    """
    list_display = ['name', 'slug', 'color', 'created_at']
    search_fields = ['name', 'description']
    prepopulated_fields = {'slug': ('name',)}


class RSSSourceInline(admin.TabularInline):
    """
    Inline RSS sources for newsletter admin.
    """
    model = RSSSource
    extra = 1
    fields = ['name', 'url', 'is_active', 'priority']


class NewsletterConfigInline(admin.StackedInline):
    """
    Inline config for newsletter admin.
    """
    model = NewsletterConfig
    can_delete = False


@admin.register(Newsletter)
class NewsletterAdmin(admin.ModelAdmin):
    """
    Newsletter admin interface.
    """
    list_display = ['title', 'owner', 'category', 'status', 'visibility', 'subscriber_count', 'created_at']
    list_filter = ['status', 'visibility', 'category', 'created_at']
    search_fields = ['title', 'short_description', 'owner__email']
    prepopulated_fields = {'slug': ('title',)}
    inlines = [NewsletterConfigInline, RSSSourceInline]
    readonly_fields = ['subscriber_count', 'total_sends', 'created_at', 'updated_at']


@admin.register(RSSSource)
class RSSSourceAdmin(admin.ModelAdmin):
    """
    RSS Source admin interface.
    """
    list_display = ['name', 'newsletter', 'url', 'is_active', 'priority', 'last_fetched']
    list_filter = ['is_active', 'newsletter']
    search_fields = ['name', 'url', 'newsletter__title']


@admin.register(Subscriber)
class SubscriberAdmin(admin.ModelAdmin):
    """
    Subscriber admin interface.
    """
    list_display = ['email', 'newsletter', 'status', 'source', 'subscribed_at']
    list_filter = ['status', 'source', 'newsletter']
    search_fields = ['email', 'newsletter__title']
    readonly_fields = ['confirmation_token', 'unsubscribe_token', 'subscribed_at', 'confirmed_at', 'unsubscribed_at']


@admin.register(SendHistory)
class SendHistoryAdmin(admin.ModelAdmin):
    """
    Send History admin interface.
    """
    list_display = ['newsletter', 'sent_at', 'recipient_count', 'success_count', 'failure_count']
    list_filter = ['newsletter', 'sent_at']
    search_fields = ['newsletter__title']
    readonly_fields = ['sent_at', 'celery_task_id']


@admin.register(EmailEvent)
class EmailEventAdmin(admin.ModelAdmin):
    """
    Email Event admin interface.
    """
    list_display = ['event_type', 'subscriber', 'send_history', 'timestamp']
    list_filter = ['event_type', 'timestamp']
    search_fields = ['subscriber__email']
    readonly_fields = ['timestamp']
