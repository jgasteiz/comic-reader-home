import collections
import os

from django.conf import settings
from django.db import transaction
from reader import domain, models


def delete_old_items():
    """
    Delete all FileItems whose paths no longer exist on disk.
    """
    missing_ids = []
    deleted_names = []
    rows = models.FileItem.objects.values_list("id", "path", "name").iterator()
    for pk, path, name in rows:
        if not os.path.exists(path):
            missing_ids.append(pk)
            deleted_names.append(name)

    if missing_ids:
        models.FileItem.objects.filter(id__in=missing_ids).delete()
        print("Deleted: %s\n" % ", ".join(deleted_names))
    else:
        print("Nothing to delete.\n")


def populate_db_from_path(path: str=settings.COMICS_SRC_PATH):
    """
    Walk the filesystem under `path` and create any missing FileItems.

    Builds the tree in memory first, then inserts level by level with
    bulk_create so each depth's parents have PKs before their children
    are written.
    """
    # depth -> list[(path, parent_path, name, file_type)]
    levels = collections.defaultdict(list)
    root_name = path.rstrip("/").split("/")[-1] or path
    levels[0].append((path, None, root_name, models.FileItem.DIRECTORY))

    queue = collections.deque([(path, 0)])
    while queue:
        current, depth = queue.popleft()
        with os.scandir(current) as entries:
            for entry in entries:
                if entry.name.startswith("."):
                    continue
                if entry.is_dir(follow_symlinks=False):
                    levels[depth + 1].append(
                        (entry.path, current, entry.name, models.FileItem.DIRECTORY)
                    )
                    queue.append((entry.path, depth + 1))
                elif domain.is_file_name_comic_file(entry.name):
                    levels[depth + 1].append(
                        (entry.path, current, entry.name, models.FileItem.COMIC)
                    )

    all_paths = [p for level in levels.values() for (p, _, _, _) in level]
    by_path = {
        fi.path: fi
        for fi in models.FileItem.objects.filter(path__in=all_paths)
    }

    created_names = []
    with transaction.atomic():
        for depth in sorted(levels):
            to_create = []
            for p, parent_path, name, file_type in levels[depth]:
                if p in by_path:
                    continue
                to_create.append(models.FileItem(
                    path=p,
                    name=name,
                    file_type=file_type,
                    parent=by_path.get(parent_path) if parent_path else None,
                ))
            if to_create:
                created = models.FileItem.objects.bulk_create(to_create)
                for fi in created:
                    by_path[fi.path] = fi
                    created_names.append(fi.name)

    if created_names:
        print("Created: %s\n" % ", ".join(created_names))
    else:
        print("Nothing new to create.\n")
