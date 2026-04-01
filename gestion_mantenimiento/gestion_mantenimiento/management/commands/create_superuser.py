from django.core.management.base import BaseCommand
from django.contrib.auth import get_user_model

class Command(BaseCommand):
    help = 'Create or update superuser'

    def handle(self, *args, **options):
        User = get_user_model()
        user, created = User.objects.get_or_create(username='admin', defaults={'email': 'admin@example.com'})
        if created:
            user.set_password('admin')
            user.is_superuser = True
            user.is_staff = True
            user.save()
            self.stdout.write(self.style.SUCCESS('Superuser created: admin / admin'))
        else:
            user.set_password('admin')
            user.is_superuser = True
            user.is_staff = True
            user.save()
            self.stdout.write(self.style.SUCCESS('Superuser updated: admin / admin'))