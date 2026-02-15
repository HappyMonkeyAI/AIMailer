from django.test import TestCase, override_settings
from django.contrib.auth import get_user_model
from django.utils import timezone
from django_celery_beat.models import PeriodicTask, CrontabSchedule
from newsletters.models import Newsletter, NewsletterConfig, Category
from newsletters.tasks import process_newsletter
from unittest.mock import patch, MagicMock

User = get_user_model()

@override_settings(CACHES={"default": {"BACKEND": "django.core.cache.backends.locmem.LocMemCache"}})
class SchedulingTests(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(email='testuser@example.com', username='testuser', password='password')
        self.category = Category.objects.create(name='Tech')
        self.newsletter = Newsletter.objects.create(
            owner=self.user,
            title='Test Newsletter',
            category=self.category,
            status='active'
        )
        self.config = NewsletterConfig.objects.create(
            newsletter=self.newsletter,
            send_schedule='0 9 * * *',  # Daily at 9am
            sender_email='test@example.com',
            sender_name='Test Sender'
        )

    def test_periodic_task_creation(self):
        """Test that creating config creates a periodic task."""
        task_name = f'process-newsletter-{self.newsletter.id}'
        # Periodic tasks are created by signals, assuming Celery Beat is set up
        # We check if the signal logic works by checking if the task exists
        self.assertTrue(PeriodicTask.objects.filter(name=task_name).exists())

        task = PeriodicTask.objects.get(name=task_name)
        self.assertTrue(task.enabled)
        self.assertEqual(task.crontab.minute, '0')
        self.assertEqual(task.crontab.hour, '9')
        # The args are stored as a JSON string
        self.assertIn(str(self.newsletter.id), task.args)

    def test_schedule_update(self):
        """Test that updating schedule updates periodic task."""
        self.config.send_schedule = '30 10 * * 1' # Mondays at 10:30
        self.config.save()

        task_name = f'process-newsletter-{self.newsletter.id}'
        task = PeriodicTask.objects.get(name=task_name)
        self.assertEqual(task.crontab.minute, '30')
        self.assertEqual(task.crontab.hour, '10')
        self.assertEqual(task.crontab.day_of_week, '1')

    def test_status_change(self):
        """Test that changing status updates enabled/disabled."""
        self.newsletter.status = 'paused'
        self.newsletter.save()

        task_name = f'process-newsletter-{self.newsletter.id}'
        task = PeriodicTask.objects.get(name=task_name)
        self.assertFalse(task.enabled)

        self.newsletter.status = 'active'
        self.newsletter.save()
        task = PeriodicTask.objects.get(name=task_name)
        self.assertTrue(task.enabled)

    def test_archive_deletes_task(self):
        """Test that archiving deletes the task."""
        self.newsletter.status = 'archived'
        self.newsletter.save()

        task_name = f'process-newsletter-{self.newsletter.id}'
        self.assertFalse(PeriodicTask.objects.filter(name=task_name).exists())

    @patch('newsletters.tasks.tracker')
    @patch('newsletters.tasks.sender')
    @patch('newsletters.tasks.composer')
    @patch('newsletters.tasks.selector')
    @patch('newsletters.tasks.summarizer')
    @patch('newsletters.tasks.extractor')
    @patch('newsletters.tasks.fetchers')
    def test_process_newsletter_task(self, mock_fetchers, mock_extractor, mock_summarizer, mock_selector, mock_composer, mock_sender, mock_tracker):
        """Test the process_newsletter task execution."""
        # Setup mocks
        mock_fetchers.fetch_rss.return_value = [{'url': 'http://example.com/1', 'title': 'Article 1'}]
        mock_fetchers.fetch_http.return_value = None  # Disable search for this test
        mock_tracker.filter_new_articles.return_value = [{'url': 'http://example.com/1', 'title': 'Article 1'}]
        mock_extractor.extract_text.return_value = "Content"
        mock_summarizer.summarize_text.return_value = {'summary': 'Summary', 'why_dev_care': 'Why', 'tags': [], 'confidence': 0.9}
        mock_selector.select_top.return_value = [{'url': 'http://example.com/1', 'title': 'Article 1', 'summary': 'Summary', 'why': 'Why', 'tags': [], 'confidence': 0.9}]
        mock_composer.compose_html.return_value = "<html>Email</html>"
        mock_sender.send_email.return_value = True

        # Ensure mark_articles_sent does nothing
        mock_tracker.mark_articles_sent.return_value = None

        # Add RSS Source and Subscriber
        from newsletters.models import Subscriber, RSSSource
        RSSSource.objects.create(newsletter=self.newsletter, url='http://example.com/rss', is_active=True)
        sub = Subscriber.objects.create(newsletter=self.newsletter, email='sub@example.com', status='active')

        # Run task
        process_newsletter(self.newsletter.id)

        # Assertions
        mock_fetchers.fetch_rss.assert_called()
        mock_tracker.filter_new_articles.assert_called()

        # Verify send_email arguments
        mock_sender.send_email.assert_called()
        args, kwargs = mock_sender.send_email.call_args

        # args[0] is subject
        # args[1] is html
        # args[2] is recipients list

        self.assertEqual(args[1], "<html>Email</html>")
        recipients = args[2]
        self.assertEqual(len(recipients), 1)
        self.assertEqual(recipients[0]['email'], 'sub@example.com')
        self.assertIn('unsubscribe_url', recipients[0])
        self.assertIn('/newsletter/unsubscribe/', recipients[0]['unsubscribe_url'])
        self.assertIn(str(sub.unsubscribe_token), recipients[0]['unsubscribe_url'])

        mock_tracker.mark_articles_sent.assert_called()

        # Verify history created
        history = self.newsletter.send_history.first()
        self.assertIsNotNone(history)
        self.assertEqual(history.success_count, 1)
