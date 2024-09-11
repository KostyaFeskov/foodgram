from django.core.management.base import BaseCommand

from django.contrib.auth import get_user_model

User = get_user_model()


class Command(BaseCommand):
    help = 'Create a superuser with predefined credentials'

    def add_arguments(self, parser):
        parser.add_argument(
            '--username',
            type=str,
            help='Username for the superuser'
        )
        parser.add_argument(
            '--email',
            type=str,
            help='Email for the superuser'
        )
        parser.add_argument(
            '--password',
            type=str,
            help='Password for the superuser'
        )
        parser.add_argument(
            '--first_name',
            type=str,
            help='First name for the superuser'
        )
        parser.add_argument(
            '--last_name',
            type=str,
            help='Last name for the superuser'
        )

    def handle(self, *args, **options):
        username = options['username']
        email = options['email']
        password = options['password']
        first_name = options['first_name']
        last_name = options['last_name']

        if User.objects.filter(username=username).exists():
            self.stdout.write(self.style.WARNING('Superuser already exists'))
        else:
            User.objects.create_superuser(
                username=username,
                email=email,
                password=password,
                first_name=first_name,
                last_name=last_name
            )
            self.stdout.write(
                self.style.SUCCESS('Superuser created successfully')
            )
