from django.core.management.base import BaseCommand
from reader.application import file_items


class Command(BaseCommand):
    help = "Populate the db with all comics and directories available."

    def handle(self, *args, **kwargs):
        file_items.extract_all_comics()
        self.stdout.write(self.style.SUCCESS("All comics have been extracted."))
