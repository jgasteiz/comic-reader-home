from reader import domain, models


def get_page_path(*, comic: models.FileItem, page_number: int) -> str:
    return domain.get_comic_page_path(
        comic=comic,
        extract_path=domain.get_extract_path_for_comic(comic),
        page_number=page_number,
    )
