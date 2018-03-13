from django.core.management.base import BaseCommand
from reader.utils import Utils


class Command(BaseCommand):
    help = 'Clears the tmp directory'

    def handle(self, *args, **kwargs):
        Utils().clear_tmp()
        self.stdout.write(self.style.SUCCESS('Tmp directory cleared successfully.'))
