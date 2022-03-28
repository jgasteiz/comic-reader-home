from django.core.management.base import BaseCommand
from reader.application import file_items


class Command(BaseCommand):
    help = "Populate the db with all comics and directories available."

    def handle(self, *args, **kwargs):
        file_items.delete_old_items()
        file_items.populate_db_from_path()
        self.stdout.write(self.style.SUCCESS("The DB has been populated."))
