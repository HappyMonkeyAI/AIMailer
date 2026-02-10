from django.test import TestCase, Client
from django.test.utils import CaptureQueriesContext
from django.contrib.auth import get_user_model
from django.urls import reverse
from newsletters.models import Newsletter, RSSSource, Category
from django.db import connection, reset_queries
import uuid

User = get_user_model()

class RSSSourceAdminPerformanceTest(TestCase):
    def setUp(self):
        self.user = User.objects.create_superuser(
            email='admin@example.com',
            password='password123',
            first_name='Admin',
            last_name='User'
        )
        self.client = Client()
        self.client.force_login(self.user)

        self.category = Category.objects.create(name='Tech', slug='tech')

        # Create multiple newsletters and RSS sources
        # We need N > a small constant to show N+1 clearly.
        # Let's use N=10.
        # Queries without optimization: ~ 2 (base) + 10 (newsletters) + extra = > 12.
        # Queries with optimization: ~ 2-5.

        for i in range(10):
            newsletter = Newsletter.objects.create(
                owner=self.user,
                title=f'Newsletter {i}',
                slug=f'newsletter-{uuid.uuid4()}', # Ensure unique slug
                category=self.category
            )
            RSSSource.objects.create(
                newsletter=newsletter,
                name=f'RSS Source {i}',
                url=f'http://example.com/rss/{i}'
            )

    def test_rss_source_changelist_queries(self):
        url = reverse('admin:newsletters_rsssource_changelist')

        # Clear existing queries just in case
        reset_queries()

        # We expect significantly less than N queries if optimized.
        # If N=10, and we assert < 10, it should fail if N+1 is present (10+ queries).
        # We'll assert < 8 to be safe and clear.
        with CaptureQueriesContext(connection) as captured:
            response = self.client.get(url)

        query_count = len(captured)
        # print(f"\nActual queries executed: {query_count}")
        # for q in captured.captured_queries:
        #     print(q['sql'])

        self.assertLess(query_count, 8, f"Expected < 8 queries, but got {query_count}. N+1 problem detected.")
        self.assertEqual(response.status_code, 200)
