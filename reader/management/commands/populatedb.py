from django.core.management.base import BaseCommand

from reader import tasks


class Command(BaseCommand):
    help = "Populate the db with all comics and directories available."

    def handle(self, *args, **kwargs):
        tasks.delete_old_items()
        tasks.populate_db_from_path()
        self.stdout.write(self.style.SUCCESS("The DB has been populated."))
