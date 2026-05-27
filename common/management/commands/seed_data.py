from django.core.management.base import BaseCommand
from django.contrib.auth import get_user_model
from django.db import transaction


class Command(BaseCommand):
    help = "Create admin account only"

    @transaction.atomic
    def handle(self, *args, **options):
        self.stdout.write("🚀 Creating admin account...")

        User = get_user_model()

        username = "admin123"
        email = "admin@hrm.local"
        password = "admin123"

        if User.objects.filter(username=username).exists():
            self.stdout.write(
                self.style.WARNING("⚠ Admin already exists")
            )
            return

        User.objects.create_superuser(
            username=username,
            email=email,
            password=password,
        )

        self.stdout.write(
            self.style.SUCCESS("✅ Admin created successfully!")
        )
        self.stdout.write(f"Username: {username}")
        self.stdout.write(f"Password: {password}")
