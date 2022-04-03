from typing import List, Optional

from reader import models as data_models

from . import models


def get_file_item(file_item_id: int) -> models.FileItem:
    instance = data_models.FileItem.objects.get(id=file_item_id)
    return _get_file_item_from_instance(instance)


def search_file_items_by_name(query: str) -> List[models.FileItem]:
    instances = data_models.FileItem.objects.filter(name__icontains=query)
    return [_get_file_item_from_instance(instance) for instance in instances]


def get_file_items_for_parent_id(parent_id: Optional[int]) -> List[models.FileItem]:
    instances = data_models.FileItem.objects.filter(parent__id=parent_id)
    return [_get_file_item_from_instance(instance) for instance in instances]


def _get_file_item_from_instance(instance: data_models.FileItem) -> models.FileItem:
    if instance.parent:
        parent = _get_file_item_from_instance(instance.parent)
    else:
        parent = None

    return models.FileItem(
        id=instance.id,
        name=instance.name,
        path=instance.path,
        file_type=models.FileType(instance.file_type),
        parent=parent,
        furthest_read_page=instance.furthest_read_page,
        is_read=instance.is_read,
        is_favorite=instance.is_favorite,
    )
