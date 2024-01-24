import os

from django.contrib.auth import get_user_model
from django.core.management.base import BaseCommand

User = get_user_model()


class Command(BaseCommand):
    def handle(self, *args, **options):
        if (email := os.getenv("SUPERUSER_EMAIL")) and (
                password := os.getenv("SUPERUSER_PASSWORD")
        ):
            self.stdout.write("Creating superuser...")

            if User.objects.filter(email=email).exists():
                self.stdout.write(self.style.SUCCESS("Superuser already exists"))
            else:
                User.objects.create_superuser(
                    email=email,
                    password=password,
                )
                self.stdout.write(self.style.SUCCESS("Superuser created successfully"))
