import os
from shutil import copyfile

from django.core.management.base import BaseCommand, CommandError
from django.utils.text import slugify

from reader.models import FileItem
from reader.utils import get_extracted_comic_pages


class Command(BaseCommand):
    help = "Extracts the given page range of each comic on a given directory."

    def add_arguments(self, parser):
        parser.add_argument(
            "file_item_id",
            metavar="file_item_id",
            type=int,
            help="Id of the collection to extract.",
        )
        parser.add_argument(
            "start_page",
            metavar="start_page",
            type=int,
            help="Initial page to be extracted",
        )
        parser.add_argument(
            "last_page", metavar="last_page", type=int, help="Last page to be extracted"
        )
        parser.add_argument(
            "extract_path",
            metavar="extract_path",
            help="Path where the pages should be extracted to",
        )

    def handle(self, *args, **options):
        file_item_id = options.get("file_item_id")
        try:
            file_item = FileItem.objects.get(pk=file_item_id)
        except FileItem.DoesNotExist:
            raise CommandError('FileItem "%s" does not exist' % file_item_id)

        extract_path = options.get("extract_path")
        initial_page_number = options.get("start_page")
        last_page_number = options.get("last_page")

        def _extract_pages(comic):
            pages = get_extracted_comic_pages(
                comic, list(range(initial_page_number, last_page_number))
            )
            for idx, page_path in enumerate(pages):
                file_name = page_path.split("/")[-1]
                file_extension = page_path.split(".")[-1]
                dst_path = os.path.join(extract_path, file_name)
                copyfile(page_path, dst_path)

                new_dst_file_name = os.path.join(
                    extract_path,
                    "%s-%d-%d.%s"
                    % (slugify(comic.name), comic.pk, idx, file_extension),
                )
                os.rename(dst_path, new_dst_file_name)

        # If we're extracting a directory, extract every comic inside.
        if file_item.file_type == FileItem.DIRECTORY:
            # Now, for each comic on the directory extract the pages on the given ranges.
            for child in file_item.children.filter(file_type=FileItem.COMIC):
                print("Extracting pages from %s" % child)
                _extract_pages(child)
        # Otherwise, just extract the comic itself
        else:
            print("Extracting pages from %s" % file_item)
            _extract_pages(file_item)
