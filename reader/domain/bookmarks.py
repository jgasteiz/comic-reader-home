from reader import models


def bookmark_page(file_item: models.FileItem, page_number: int):
    """
    Create or update and existing bookmark for this comic
    on the given page number.
    """
    if file_item.file_type == file_item.COMIC:
        if hasattr(file_item, "bookmark"):
            bookmark = models.Bookmark.objects.get(comic_id=file_item.pk)
            bookmark.page_number = page_number
            bookmark.save(update_fields=["page_number"])
        else:
            models.Bookmark.objects.create(
                comic_id=file_item.pk, page_number=page_number
            )


def delete_bookmark(file_item: models.FileItem):
    if file_item.file_type == file_item.COMIC:
        if hasattr(file_item, "bookmark"):
            bookmark = models.Bookmark.objects.get(comic_id=file_item.pk)
            bookmark.delete()
