import logging
import os
from typing import List, Optional, Union
from zipfile import BadZipFile, ZipFile

from django.conf import settings
from django.core.cache import cache
from rarfile import BadRarFile, RarFile
from reader import models


class UnableToExtractPage(Exception):
    pass


def get_next_comic_in_directory(
    comic: models.FileItem,
) -> Optional[models.FileItem]:
    """
    Next sibling comic in the same directory, ordered by name. None if
    the comic has no parent or is the last one in its directory.
    """
    if comic.parent is None:
        return None
    return (
        models.FileItem.objects.comics()
        .filter(parent=comic.parent, name__gt=comic.name)
        .order_by("name")
        .first()
    )


def get_num_pages(file_item: models.FileItem) -> int:
    """
    Get the number of pages of a comic.
    """
    if not file_item.is_comic:
        return 0
    return len(_get_page_names_for_comic(file_item))


def is_file_name_comic_file(file_name: str) -> bool:
    """
    Checks whether a given file name is a valid comic file name.
    """
    if not _is_file_name_cbz(file_name) and not _is_file_name_cbr(file_name):
        return False
    if _is_file_name_a_hidden_file(file_name):
        return False
    return True


def get_comic_page_path(
    *, comic: models.FileItem, extract_path: str, page_number: int
) -> str:
    """
    Extract the given page number or do nothing if it has been extracted already.
    """
    page_names = _get_page_names_for_comic(comic)

    try:
        page_file_name = page_names[page_number]
    except IndexError:
        raise UnableToExtractPage(f"The page {page_number} could not be extracted.")

    page_file_path = os.path.join(extract_path, page_file_name)

    # If it exists already, return it without touching the archive.
    if os.path.exists(page_file_path):
        logging.info("Page exists, no need to extract it.")
        return page_file_path

    # Otherwise, open the archive and extract.
    if not os.path.exists(extract_path):
        os.makedirs(extract_path)
    try:
        cb_file = get_cb_file_for_comic(comic)
        cb_file.extract(page_file_name, extract_path)
    except (BadZipFile, BadRarFile) as e:
        raise UnableToExtractPage(
            f"Could not extract page {page_number} from {comic.name}: {e}"
        )
    return page_file_path


def get_extract_path_for_comic(comic: models.FileItem) -> str:
    return os.path.join(settings.COMICS_EXTRACT_PATH, str(comic.pk))


def get_cb_file_for_comic(comic: models.FileItem) -> Union[ZipFile, RarFile]:
    if _is_file_name_cbz(comic.name):
        return ZipFile(comic.path)
    elif _is_file_name_cbr(comic.name):
        return RarFile(comic.path)
    else:
        raise TypeError(f"Unable to get a cb file for {comic}")


def _get_page_names_for_comic(comic: models.FileItem) -> List[str]:
    """
    Cached list of page filenames inside a comic's archive.

    Avoids re-opening the archive on every page request — opening a CBR
    in particular is expensive because rarfile shells out to `unrar`.
    """
    cache_key = f"page_names_{comic.pk}"
    cached = cache.get(cache_key)
    if cached is not None:
        return cached
    try:
        cb_file = get_cb_file_for_comic(comic)
        page_names = _get_comic_pages(cb_file)
    except (BadZipFile, BadRarFile) as e:
        raise UnableToExtractPage(f"Could not read archive for {comic.name}: {e}")
    cache.set(cache_key, page_names)
    return page_names


def _get_comic_pages(cb_file: Union[ZipFile, RarFile]) -> List[str]:
    pages = [
        p
        for p in cb_file.namelist()
        if p.lower().endswith((".jpg", ".jpeg", ".png"))
        and not p.split("/")[-1].startswith(".")
    ]
    return sorted(pages)


def _is_file_name_cbz(file_name: str) -> bool:
    return file_name.endswith(".cbz")


def _is_file_name_cbr(file_name: str) -> bool:
    return file_name.endswith(".cbr")


def _is_file_name_a_hidden_file(file_name: str) -> bool:
    return file_name.startswith(".")
