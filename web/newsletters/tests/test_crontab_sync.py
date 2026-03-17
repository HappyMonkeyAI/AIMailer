from django.test import TestCase
from django.contrib.auth import get_user_model
from django_celery_beat.models import PeriodicTask, CrontabSchedule
from newsletters.models import Newsletter, NewsletterConfig, Category
import json

User = get_user_model()

class CrontabSyncTests(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(email='sync@example.com', username='syncuser', password='password')
        self.category = Category.objects.create(name='Sync')
        self.newsletter = Newsletter.objects.create(
            owner=self.user,
            title='Sync Newsletter',
            category=self.category,
            status='active'
        )
        self.config = NewsletterConfig.objects.create(
            newsletter=self.newsletter,
            send_schedule='00 09 * * *',  # Note '00'
            sender_email='sync@example.com',
            sender_name='Sync Sender'
        )

    def test_normalization_and_deduplication(self):
        """Test that '00' is normalized to '0' and reused."""
        self.config.refresh_from_db()
        # Verify it was normalized to '0 9 * * *'
        self.assertEqual(self.config.send_schedule, '0 9 * * *')
        
        # Verify CrontabSchedule has '0'
        task = PeriodicTask.objects.get(name=f'process-newsletter-{self.newsletter.id}')
        self.assertEqual(task.crontab.minute, '0')

        # Create another newsletter with '0 9 * * *'
        newsletter2 = Newsletter.objects.create(
            owner=self.user, title='Other', category=self.category, status='active'
        )
        config2 = NewsletterConfig.objects.create(
            newsletter=newsletter2,
            send_schedule='0 09 * * *',
            sender_email='other@example.com',
            sender_name='Other'
        )
        
        # Should reuse the same CrontabSchedule
        task2 = PeriodicTask.objects.get(name=f'process-newsletter-{newsletter2.id}')
        self.assertEqual(task.crontab.id, task2.crontab.id)

    def test_back_sync(self):
        """Test that updating CrontabSchedule updates NewsletterConfig."""
        task = PeriodicTask.objects.get(name=f'process-newsletter-{self.newsletter.id}')
        crontab = task.crontab
        
        # Update the crontab directly
        crontab.hour = '13'
        crontab.save()
        
        self.config.refresh_from_db()
        self.assertEqual(self.config.send_schedule, '0 13 * * *')
