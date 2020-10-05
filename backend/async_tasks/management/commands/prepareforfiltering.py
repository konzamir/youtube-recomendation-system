from django.core.management.base import BaseCommand


class Command(BaseCommand):
    help = 'Command for updating process status, when all videos will be checked'

    def handle(self, *args, **options):
        pass
