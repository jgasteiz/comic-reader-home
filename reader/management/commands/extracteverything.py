from django.core.management.base import BaseCommand

from reader.utils import extract_everything


class Command(BaseCommand):
    help = "Extracts all comics in the system so we don't do syncrhonous zip/rar extractions."

    def handle(self, *args, **kwargs):
        extract_everything()
        self.stdout.write(self.style.SUCCESS("Everything has been extracted."))
