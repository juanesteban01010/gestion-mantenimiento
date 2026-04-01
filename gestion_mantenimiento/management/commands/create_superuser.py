from django.core.management.base import BaseCommand
from django.contrib.auth.models import User, Group

GROUPS = ['Admin', 'Cliente', 'Tecnico']

class Command(BaseCommand):
    help = 'Create superuser if it does not exist and ensure groups exist'

    def handle(self, *args, **options):
        # Ensure all required groups exist
        for group_name in GROUPS:
            group, group_created = Group.objects.get_or_create(name=group_name)
            if group_created:
                self.stdout.write(self.style.SUCCESS(f'Group created: {group_name}'))

        # Create or update the superuser
        if not User.objects.filter(username='juanesteban01010').exists():
            user = User.objects.create_superuser(
                username='juanesteban01010',
                email='juanesteban01010@example.com',
                password='r3g1n4jK',
            )
            self.stdout.write(self.style.SUCCESS('Superuser created successfully'))
        else:
            user = User.objects.get(username='juanesteban01010')
            user.set_password('r3g1n4jK')
            user.save()
            self.stdout.write(self.style.SUCCESS('Superuser password updated'))

        # Assign the superuser to all groups so it can log in with any account type
        for group_name in GROUPS:
            group = Group.objects.get(name=group_name)
            user.groups.add(group)

        self.stdout.write(self.style.SUCCESS('Superuser assigned to groups: ' + ', '.join(GROUPS)))