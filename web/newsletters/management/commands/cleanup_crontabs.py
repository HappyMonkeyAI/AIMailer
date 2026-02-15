from django.core.management.base import BaseCommand
from django_celery_beat.models import CrontabSchedule, PeriodicTask
from newsletters.models import NewsletterConfig
import json

class Command(BaseCommand):
    help = 'Cleanup orphan and duplicate CrontabSchedules'

    def handle(self, *args, **options):
        self.stdout.write("Starting CrontabSchedule cleanup...")

        # 1. Normalize all existing CrontabSchedules (remove leading zeros)
        all_crons = CrontabSchedule.objects.all()
        for cron in all_crons:
            changed = False
            for field in ['minute', 'hour', 'day_of_month', 'month_of_year', 'day_of_week']:
                val = getattr(cron, field)
                if val.isdigit() and val != str(int(val)):
                    setattr(cron, field, str(int(val)))
                    changed = True
            if changed:
                try:
                    cron.save()
                    self.stdout.write(f"Normalized CrontabSchedule {cron.id}")
                except Exception as e:
                    self.stdout.write(self.style.ERROR(f"Error normalizing CrontabSchedule {cron.id}: {e}"))

        # 2. Merge Duplicates
        unique_crons = {} # (m, h, d, M, dw) -> primary_cron_id
        all_crons = CrontabSchedule.objects.all().order_by('id')
        
        for cron in all_crons:
            key = (cron.minute, cron.hour, cron.day_of_month, cron.month_of_year, cron.day_of_week)
            if key not in unique_crons:
                unique_crons[key] = cron
            else:
                primary = unique_crons[key]
                self.stdout.write(f"Found duplicate: CrontabSchedule {cron.id} matches {primary.id}. Merging...")
                
                # Update PeriodicTasks to use the primary one
                tasks_updated = PeriodicTask.objects.filter(crontab=cron).update(crontab=primary)
                self.stdout.write(f"  Updated {tasks_updated} PeriodicTasks")
                
                # Delete the duplicate
                cron.delete()

        # 3. Remove Orphans (not linked to any PeriodicTask)
        # Note: We should be careful about system crontabs if any, but usually they are linked.
        # PeriodicTask.objects.all() includes celery.backend_cleanup
        all_crons = CrontabSchedule.objects.all()
        for cron in all_crons:
            if not PeriodicTask.objects.filter(crontab=cron).exists():
                self.stdout.write(f"Removing orphan CrontabSchedule {cron.id}: {cron}")
                cron.delete()

        self.stdout.write(self.style.SUCCESS("Cleanup complete."))
