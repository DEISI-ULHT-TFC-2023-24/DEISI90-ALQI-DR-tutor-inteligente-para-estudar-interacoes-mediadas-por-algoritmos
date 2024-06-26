import subprocess
import logging
from django.core.management.base import BaseCommand
from django.contrib.auth.models import User


class Command(BaseCommand):
    help = 'Create a superuser if it does not exist'

    def handle(self, *args, **options):
        username = "admin"
        email = "admin@admin.com"
        password = "admin"

        if not User.objects.filter(username=username).exists():
            User.objects.create_superuser(username, email, password)
            print('Superuser created successfully')
        else:
            print('Superuser already exists')


