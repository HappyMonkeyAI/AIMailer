from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver
from django_celery_beat.models import PeriodicTask, CrontabSchedule
import json
import logging
from django.core.exceptions import ObjectDoesNotExist

from .models import NewsletterConfig, Newsletter

logger = logging.getLogger(__name__)

def update_newsletter_task(newsletter):
    """
    Update or create the periodic task for a newsletter.
    """
    try:
        config = newsletter.config
    except ObjectDoesNotExist:
        # Config doesn't exist yet, skip
        return

    schedule_str = config.send_schedule

    # Task name should be unique and identifiable
    # Using 'process-newsletter-{id}'
    task_name = f'process-newsletter-{newsletter.id}'

    # If archived or paused, disable or delete task
    # If status is not active, we disable it.
    enabled = newsletter.status == 'active'

    if newsletter.status == 'archived':
        # Clean up task if archived
        PeriodicTask.objects.filter(name=task_name).delete()
        return

    try:
        # Parse cron expression: minute hour day_of_month month_of_year day_of_week
        parts = schedule_str.split()
        if len(parts) != 5:
            logger.warning(f"Invalid cron expression for newsletter {newsletter.id}: {schedule_str}")
            return

        minute, hour, day_of_month, month_of_year, day_of_week = parts

        schedule, _ = CrontabSchedule.objects.get_or_create(
            minute=minute,
            hour=hour,
            day_of_month=day_of_month,
            month_of_year=month_of_year,
            day_of_week=day_of_week,
        )

        PeriodicTask.objects.update_or_create(
            name=task_name,
            defaults={
                'crontab': schedule,
                'task': 'newsletters.tasks.process_newsletter',
                'args': json.dumps([newsletter.id]),
                'enabled': enabled,
                'description': f'Process newsletter: {newsletter.title}'
            }
        )
        logger.info(f"Updated schedule for newsletter {newsletter.id} (enabled={enabled})")

    except Exception as e:
        logger.error(f"Error updating schedule for newsletter {newsletter.id}: {e}")


@receiver(post_save, sender=NewsletterConfig)
def config_saved(sender, instance, created, **kwargs):
    # instance is NewsletterConfig
    try:
        newsletter = instance.newsletter
        update_newsletter_task(newsletter)
    except Exception as e:
        logger.error(f"Error in config_saved signal: {e}")

@receiver(post_save, sender=Newsletter)
def newsletter_saved(sender, instance, created, **kwargs):
    # instance is Newsletter
    update_newsletter_task(instance)

@receiver(post_delete, sender=Newsletter)
def newsletter_deleted(sender, instance, **kwargs):
    task_name = f'process-newsletter-{instance.id}'
    PeriodicTask.objects.filter(name=task_name).delete()
