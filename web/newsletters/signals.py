from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver
from django_celery_beat.models import PeriodicTask, CrontabSchedule
import json
import logging
from django.core.exceptions import ObjectDoesNotExist

from .models import NewsletterConfig, Newsletter, Subscriber

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

        # Normalize parts (e.g., '0' to '0')
        def normalize_part(p):
            try:
                # If it's a simple integer, strip leading zeros
                if p.isdigit():
                    return str(int(p))
            except:
                pass
            return p

        minute, hour, day_of_month, month_of_year, day_of_week = [normalize_part(p) for p in parts]

        schedule, _ = CrontabSchedule.objects.get_or_create(
            minute=minute,
            hour=hour,
            day_of_month=day_of_month,
            month_of_year=month_of_year,
            day_of_week=day_of_week,
        )

        # Update the config string to match the normalized version
        normalized_schedule = f"{minute} {hour} {day_of_month} {month_of_year} {day_of_week}"
        if config.send_schedule != normalized_schedule:
            NewsletterConfig.objects.filter(id=config.id).update(send_schedule=normalized_schedule)

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

@receiver(post_save, sender=Subscriber)
def subscriber_saved(sender, instance, created, **kwargs):
    """Update subscriber count when a subscriber is added or updated."""
    newsletter = instance.newsletter
    count = newsletter.subscribers.filter(status='active').count()
    if newsletter.subscriber_count != count:
        Newsletter.objects.filter(id=newsletter.id).update(subscriber_count=count)

@receiver(post_delete, sender=Subscriber)
def subscriber_deleted(sender, instance, **kwargs):
    """Update subscriber count when a subscriber is removed."""
    newsletter = instance.newsletter
    count = newsletter.subscribers.filter(status='active').count()
    if newsletter.subscriber_count != count:
        Newsletter.objects.filter(id=newsletter.id).update(subscriber_count=count)

@receiver(post_save, sender=CrontabSchedule)
def crontab_saved(sender, instance, **kwargs):
    """
    When a CrontabSchedule is updated, sync it back to any linked Newsletters.
    """
    # Find all newsletter tasks using this schedule
    tasks = PeriodicTask.objects.filter(
        crontab=instance,
        task='newsletters.tasks.process_newsletter'
    )

    new_schedule = f"{instance.minute} {instance.hour} {instance.day_of_month} {instance.month_of_year} {instance.day_of_week}"

    for task in tasks:
        try:
            # Task args is a JSON list [newsletter_id]
            newsletter_id = json.loads(task.args)[0]
            # Update the config directly to avoid triggering update_newsletter_task again
            NewsletterConfig.objects.filter(newsletter_id=newsletter_id).update(send_schedule=new_schedule)
            logger.info(f"Synced CrontabSchedule change back to Newsletter {newsletter_id}")
        except Exception as e:
            logger.error(f"Error syncing CrontabSchedule {instance.id} to task {task.name}: {e}")
