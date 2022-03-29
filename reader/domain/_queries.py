import logging
import os
from typing import List, Union
from zipfile import ZipFile

from django.conf import settings
from django.core.cache import cache
from rarfile import RarFile
from reader import models


class UnableToExtractPage(Exception):
    pass


def get_num_pages(file_item: models.FileItem) -> int:
    """
    Get the number of pages of a comic.
    """
    cache_key = f"num_pages_{file_item.pk}"
    if cache.get(cache_key):
        return cache.get(cache_key)

    # Ensure the given FileItem is a comic.
    if not file_item.is_comic:
        cache.set(cache_key, 0)
        return 0

    cb_file = get_cb_file_for_comic(file_item)
    num_pages = len(_get_comic_pages(cb_file))
    cache.set(cache_key, num_pages)
    return num_pages


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
    *, cb_file: Union[ZipFile, RarFile], extract_path: str, page_number: int
) -> str:
    """
    Extract the given page number or do nothing if it has been extracted already.
    """
    comic_pages = _get_comic_pages(cb_file)

    try:
        page_file_name = comic_pages[page_number]
    except IndexError:
        raise UnableToExtractPage(f"The page {page_number} could not be extracted.")

    page_file_path = os.path.join(extract_path, page_file_name)

    # If it exists already, return it.
    if os.path.exists(page_file_path):
        logging.info("Page exists, no need to extract it.")
        return page_file_path

    # Otherwise, extract it.
    if not os.path.exists(extract_path):
        os.makedirs(extract_path)
    cb_file.extract(page_file_name, extract_path)
    return page_file_path


def get_comic_page_paths(
    *, cb_file: Union[ZipFile, RarFile], extract_path: str
) -> List[str]:
    """
    Extract all pages of a comic.
    """
    if not os.path.exists(extract_path):
        os.makedirs(extract_path)

    page_file_paths = []
    for page_file_name in _get_comic_pages(cb_file):
        page_file_path = os.path.join(extract_path, page_file_name)

        if not os.path.exists(page_file_path):
            cb_file.extract(page_file_name, extract_path)

        page_file_paths.append(page_file_path)

    return page_file_paths


def get_extract_path_for_comic(comic: models.FileItem) -> str:
    return os.path.join(settings.COMICS_EXTRACT_PATH, str(comic.pk))


def get_cb_file_for_comic(comic: models.FileItem) -> Union[ZipFile, RarFile]:
    if _is_file_name_cbz(comic.name):
        return ZipFile(comic.path)
    elif _is_file_name_cbr(comic.name):
        return RarFile(comic.path)
    else:
        raise TypeError(f"Unable to get a cb file for {comic}")


def _get_comic_pages(cb_file: Union[ZipFile, RarFile]) -> List[str]:
    all_pages = sorted(
        [
            p
            for p in cb_file.namelist()
            if p.endswith(".jpg") or p.endswith(".jpeg") or p.endswith(".png")
        ]
    )
    # Remove hidden files (files that start with `.`) from the pages list.
    return list(filter(lambda x: not x.split("/")[-1].startswith("."), all_pages))


def _is_file_name_cbz(file_name: str) -> bool:
    return file_name.endswith(".cbz")


def _is_file_name_cbr(file_name: str) -> bool:
    return file_name.endswith(".cbr")


def _is_file_name_a_hidden_file(file_name: str) -> bool:
    return file_name.startswith(".")
