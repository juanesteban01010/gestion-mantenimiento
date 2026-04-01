from django.core.management.base import BaseCommand
from django.contrib.auth import get_user_model


class Command(BaseCommand):
    help = 'Create a default superuser (admin/admin) if it does not already exist'

    def handle(self, *args, **options):
        User = get_user_model()

        if User.objects.filter(username='admin').exists():
            self.stdout.write(self.style.WARNING(
                'Default superuser "admin" already exists — skipping creation.'
            ))
            return

        User.objects.create_superuser(
            username='admin',
            email='admin@localhost',
            password='admin',
        )
        self.stdout.write(self.style.SUCCESS(
            'Default superuser created: username=admin / password=admin'
        ))
