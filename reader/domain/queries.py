from typing import Optional

from . import models, repository


def get_directory_details(
    parent_id: Optional[int] = None, query: Optional[str] = ""
) -> models.DirectoryDetails:
    if query:
        return _get_search_results(query)
    else:
        return _get_directory_details_for_parent_id(parent_id)


def _get_search_results(query: str) -> models.DirectoryDetails:
    return models.DirectoryDetails(
        file_items=repository.search_file_items_by_name(query),
        parent=None,
    )


def _get_directory_details_for_parent_id(
    parent_id: Optional[int],
) -> models.DirectoryDetails:
    return models.DirectoryDetails(
        file_items=repository.get_file_items_for_parent_id(parent_id),
        parent=get_file_item(parent_id),
    )


def get_file_item(file_item_id: Optional[int]) -> Optional[models.FileItem]:
    if file_item_id:
        return repository.get_file_item(file_item_id)
    else:
        return None
