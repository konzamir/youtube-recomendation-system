from django.core.management.base import BaseCommand, CommandError, CommandParser


class Command(BaseCommand):
    help = ''

    def add_arguments(self, parser: CommandParser):
        pass

    def handle(self, *args, **options):
        pass
