import logging
from subprocess import PIPE, Popen

from django.contrib.staticfiles.management.commands import runserver


class Command(runserver.Command):
    help = (
        "Starts a lightweight Web server for development and also serves static files."
    )

    def run(self, *args, **options):
        watch_proc = None
        watch_proc = Popen(["yarn", "run", "webpack-watch"])
        try:
            logging.info("Starting localhost:")
            super(Command, self).run(*args, **options)
        except (BaseException, Exception) as e:
            try:
                if watch_proc:
                    watch_proc.kill()
            except OSError:
                pass
            raise e
