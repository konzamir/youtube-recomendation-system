from django.core.management.base import BaseCommand


class Command(BaseCommand):
    help = 'Command for filtering videos per process'

    def handle(self, *args, **options):
        pass
