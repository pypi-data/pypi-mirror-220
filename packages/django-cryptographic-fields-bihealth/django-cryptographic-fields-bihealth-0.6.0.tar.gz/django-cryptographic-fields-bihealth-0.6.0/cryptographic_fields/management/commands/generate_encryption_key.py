import cryptography.fernet
from django.core.management.base import BaseCommand


class Command(BaseCommand):
    help = "Generates a new Fernet encryption key"

    def handle(self, *args, **options):
        key = cryptography.fernet.Fernet.generate_key()
        self.stdout.write(key)
