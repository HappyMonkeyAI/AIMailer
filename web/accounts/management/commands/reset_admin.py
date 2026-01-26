import argparse
from django.core.management.base import BaseCommand
from accounts.models import CustomUser

class Command(BaseCommand):
    help = 'Reset admin password or create a new superuser'

    def add_arguments(self, parser):
        parser.add_argument('email', type=str, help='Email of the superuser')
        parser.add_argument('--password', type=str, help='New password for the superuser')
        parser.add_argument('--username', type=str, default='admin', help='Username for the superuser (default: admin)')

    def handle(self, *args, **options):
        email = options['email']
        password = options['password']
        username = options['username']

        user, created = CustomUser.objects.get_or_create(
            email=email,
            defaults={
                'username': username,
                'is_staff': True,
                'is_superuser': True,
                'is_active': True,
            }
        )

        if created:
            if not password:
                self.stdout.write(self.style.ERROR(f'Superuser {email} created, but no password provided!'))
            else:
                user.set_password(password)
                user.save()
                self.stdout.write(self.style.SUCCESS(f'Successfully created superuser {email}'))
        else:
            if password:
                user.set_password(password)
                user.save()
                self.stdout.write(self.style.SUCCESS(f'Successfully updated password for superuser {email}'))
            else:
                self.stdout.write(self.style.WARNING(f'Superuser {email} already exists. No changes made.'))
