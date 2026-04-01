from django.core.management.base import BaseCommand
from django.contrib.auth import get_user_model

class Command(BaseCommand):
    help = 'Create or update superuser'

    def handle(self, *args, **options):
        User = get_user_model()
        user, created = User.objects.get_or_create(username='juanesteban01010', defaults={'email': 'juanesteban01010@example.com'})
        user.set_password('r3g1n4jK')
        user.is_superuser = True
        user.is_staff = True
        user.save()
        if created:
            self.stdout.write(self.style.SUCCESS('Superuser created: juanesteban01010 / r3g1n4jK'))
        else:
            self.stdout.write(self.style.SUCCESS('Superuser updated: juanesteban01010 / r3g1n4jK'))