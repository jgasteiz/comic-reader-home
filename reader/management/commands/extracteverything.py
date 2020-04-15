from django.core.management.base import BaseCommand

from reader.domain import file_handler


class Command(BaseCommand):
    help = "Extracts all comics in the system so we don't do syncrhonous zip/rar extractions."

    def handle(self, *args, **kwargs):
        file_handler.extract_everything()
        self.stdout.write(self.style.SUCCESS("Everything has been extracted."))
