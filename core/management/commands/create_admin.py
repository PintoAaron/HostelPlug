from django.core.management.base import BaseCommand
from core.models import User
from django.db import connection
import os


class Command(BaseCommand):
    help = 'Create admin user'

    def handle(self, *args, **kwargs):
        username = os.getenv('ADMIN_USERNAME')
        email = os.getenv('ADMIN_EMAIL')
        password = os.getenv('ADMIN_PASSWORD')
        with connection.cursor() as cursor:
            cursor.execute(f"SELECT * FROM core_user WHERE username='{username}'")
            result = cursor.fetchone()
            if result:
                self.stdout.write(self.style.SUCCESS('Admin user already exists'))
            else:
                User.objects.create_superuser(username=username, email=email, password=password)
                self.stdout.write(self.style.SUCCESS('Admin user created successfully'))