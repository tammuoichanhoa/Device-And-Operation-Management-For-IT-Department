from django.core.management.base import BaseCommand
from django.contrib.auth import get_user_model

class Command(BaseCommand):
    help = 'Tạo superuser tự động'

    def add_arguments(self, parser):
        parser.add_argument('--username', type=str, required=True)
        parser.add_argument('--password', type=str, required=True)

    def handle(self, *args, **options):
        User = get_user_model()
        username = options['username']
        password = options['password']

        if not User.objects.filter(username=username).exists():
            User.objects.create_superuser(username=username, password=password)
            self.stdout.write(self.style.SUCCESS(f'Superuser "{username}" created.'))
        else:
            self.stdout.write(self.style.WARNING(f'Superuser "{username}" already exists.'))
