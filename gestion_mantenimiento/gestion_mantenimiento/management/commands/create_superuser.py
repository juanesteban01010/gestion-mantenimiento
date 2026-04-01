from django.core.management.base import BaseCommand
from django.contrib.auth import get_user_model
from django.contrib.auth.models import Group

GROUPS = ['Admin', 'Cliente', 'Tecnico']

class Command(BaseCommand):
    help = 'Create or update superuser and ensure groups exist'

    def handle(self, *args, **options):
        User = get_user_model()

        # Ensure all required groups exist
        for group_name in GROUPS:
            group, group_created = Group.objects.get_or_create(name=group_name)
            if group_created:
                self.stdout.write(self.style.SUCCESS(f'Group created: {group_name}'))

        # Create or update the superuser
        user, created = User.objects.get_or_create(
            username='juanesteban01010',
            defaults={'email': 'juanesteban01010@example.com'},
        )
        user.set_password('r3g1n4jK')
        user.is_superuser = True
        user.is_staff = True
        user.save()

        # Assign the superuser to all groups so it can log in with any account type
        for group_name in GROUPS:
            group = Group.objects.get(name=group_name)
            user.groups.add(group)

        if created:
            self.stdout.write(self.style.SUCCESS('Superuser created: juanesteban01010 / r3g1n4jK'))
        else:
            self.stdout.write(self.style.SUCCESS('Superuser updated: juanesteban01010 / r3g1n4jK'))

        self.stdout.write(self.style.SUCCESS('Superuser assigned to groups: ' + ', '.join(GROUPS)))