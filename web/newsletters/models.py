"""
Newsletter models for AIMailer.
"""
from django.db import models
from django.conf import settings
from django.utils.text import slugify
from django.utils.translation import gettext_lazy as _
import uuid


class Category(models.Model):
    """
    Newsletter categories for organization and discovery.
    """
    name = models.CharField(max_length=100, unique=True)
    slug = models.SlugField(max_length=100, unique=True)
    description = models.TextField(blank=True)
    icon = models.CharField(max_length=50, blank=True)
    color = models.CharField(max_length=7, default='#3B82F6')
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        verbose_name_plural = 'categories'
        ordering = ['name']
    
    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        super().save(*args, **kwargs)
    
    def __str__(self):
        return self.name


class Newsletter(models.Model):
    """
    Core newsletter entity.
    """
    STATUS_CHOICES = [
        ('draft', 'Draft'),
        ('active', 'Active'),
        ('paused', 'Paused'),
        ('archived', 'Archived'),
    ]
    
    VISIBILITY_CHOICES = [
        ('public', 'Public'),
        ('private', 'Private'),
        ('unlisted', 'Unlisted'),
    ]
    
    owner = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='newsletters'
    )
    title = models.CharField(max_length=255)
    slug = models.SlugField(max_length=255, unique=True)
    short_description = models.CharField(max_length=500)
    long_description = models.TextField()
    category = models.ForeignKey(
        Category,
        on_delete=models.SET_NULL,
        null=True,
        related_name='newsletters'
    )
    keywords = models.JSONField(
        default=list, 
        blank=True, 
        help_text=_('Comma-separated list of keywords for article selection (e.g., "ai, agent, mcp").')
    )
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='draft')
    visibility = models.CharField(max_length=20, choices=VISIBILITY_CHOICES, default='public')
    logo = models.ImageField(upload_to='newsletter_logos/', blank=True, null=True)
    banner = models.ImageField(upload_to='newsletter_banners/', blank=True, null=True)
    
    # Denormalized counts for performance
    subscriber_count = models.IntegerField(default=0)
    total_sends = models.IntegerField(default=0)
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        ordering = ['-created_at']
        indexes = [
            models.Index(fields=['status', 'visibility']),
            models.Index(fields=['slug']),
        ]
    
    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.title)
        super().save(*args, **kwargs)
    
    def __str__(self):
        return self.title


class NewsletterConfig(models.Model):
    """
    Configuration settings for each newsletter.
    """
    newsletter = models.OneToOneField(
        Newsletter,
        on_delete=models.CASCADE,
        related_name='config'
    )
    send_schedule = models.CharField(
        max_length=100, 
        help_text=_('Cron expression (e.g., "0 9 * * *" for daily at 9am, "0 10 * * 1" for Mondays at 10am).')
    )
    article_count = models.IntegerField(default=12)
    email_template = models.CharField(max_length=100, default='default')
    sender_name = models.CharField(max_length=255)
    sender_email = models.EmailField()
    reply_to_email = models.EmailField(blank=True)
    ai_summary_enabled = models.BooleanField(default=True)
    config_json = models.JSONField(
        default=dict, 
        help_text=_('Advanced settings as JSON. Common keys: "email_subject", "dry_run" (bool), "source_weights" (dict of domain:weight).')
    )
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return f"Config for {self.newsletter.title}"


class RSSSource(models.Model):
    """
    RSS feed sources for newsletters.
    """
    newsletter = models.ForeignKey(
        Newsletter,
        on_delete=models.CASCADE,
        related_name='rss_sources'
    )
    name = models.CharField(max_length=255)
    url = models.URLField()
    description = models.TextField(blank=True)
    is_active = models.BooleanField(default=True)
    priority = models.IntegerField(default=1, help_text='Weight for article selection')
    last_fetched = models.DateTimeField(null=True, blank=True)
    fetch_frequency = models.IntegerField(default=60, help_text='Minutes between fetches')
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        ordering = ['-priority', 'name']
        verbose_name = 'RSS Source'
        verbose_name_plural = 'RSS Sources'
    
    def __str__(self):
        return f"{self.name} ({self.newsletter.title})"


class Subscriber(models.Model):
    """
    Newsletter subscribers.
    """
    STATUS_CHOICES = [
        ('pending', 'Pending Confirmation'),
        ('active', 'Active'),
        ('unsubscribed', 'Unsubscribed'),
        ('bounced', 'Bounced'),
    ]
    
    SOURCE_CHOICES = [
        ('web', 'Web Signup'),
        ('api', 'API'),
        ('import', 'CSV Import'),
    ]
    
    newsletter = models.ForeignKey(
        Newsletter,
        on_delete=models.CASCADE,
        related_name='subscribers'
    )
    email = models.EmailField()
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')
    source = models.CharField(max_length=20, choices=SOURCE_CHOICES, default='web')
    
    # Tokens
    confirmation_token = models.UUIDField(default=uuid.uuid4, editable=False)
    unsubscribe_token = models.UUIDField(default=uuid.uuid4, editable=False, unique=True)
    
    # Timestamps
    subscribed_at = models.DateTimeField(auto_now_add=True)
    confirmed_at = models.DateTimeField(null=True, blank=True)
    unsubscribed_at = models.DateTimeField(null=True, blank=True)
    
    # Custom fields for extensibility
    custom_fields = models.JSONField(default=dict, blank=True)
    
    class Meta:
        unique_together = ['newsletter', 'email']
        ordering = ['-subscribed_at']
        indexes = [
            models.Index(fields=['email', 'status']),
            models.Index(fields=['unsubscribe_token']),
        ]
    
    def __str__(self):
        return f"{self.email} - {self.newsletter.title}"


class SendHistory(models.Model):
    """
    Track newsletter send history.
    """
    newsletter = models.ForeignKey(
        Newsletter,
        on_delete=models.CASCADE,
        related_name='send_history'
    )
    sent_at = models.DateTimeField(auto_now_add=True)
    recipient_count = models.IntegerField(default=0)
    success_count = models.IntegerField(default=0)
    failure_count = models.IntegerField(default=0)
    articles_sent = models.JSONField(default=list)
    celery_task_id = models.CharField(max_length=255, blank=True)
    
    class Meta:
        ordering = ['-sent_at']
        verbose_name_plural = 'send histories'
    
    def __str__(self):
        return f"{self.newsletter.title} - {self.sent_at.strftime('%Y-%m-%d %H:%M')}"


class EmailEvent(models.Model):
    """
    Track email events (opens, clicks, bounces, etc.).
    """
    EVENT_TYPES = [
        ('sent', 'Sent'),
        ('delivered', 'Delivered'),
        ('opened', 'Opened'),
        ('clicked', 'Clicked'),
        ('bounced', 'Bounced'),
        ('complained', 'Complained'),
    ]
    
    send_history = models.ForeignKey(
        SendHistory,
        on_delete=models.CASCADE,
        related_name='events'
    )
    subscriber = models.ForeignKey(
        Subscriber,
        on_delete=models.CASCADE,
        related_name='email_events'
    )
    event_type = models.CharField(max_length=20, choices=EVENT_TYPES)
    timestamp = models.DateTimeField(auto_now_add=True)
    metadata = models.JSONField(default=dict, blank=True)
    
    class Meta:
        ordering = ['-timestamp']
        indexes = [
            models.Index(fields=['event_type', 'timestamp']),
        ]
    
    def __str__(self):
        return f"{self.event_type} - {self.subscriber.email}"


class SentArticle(models.Model):
    """
    Track sent article URLs to avoid duplicates.
    """
    url = models.URLField(unique=True, db_index=True, max_length=2000)
    sent_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-sent_at']
        verbose_name = 'Sent Article'
        verbose_name_plural = 'Sent Articles'

    def __str__(self):
        return self.url
