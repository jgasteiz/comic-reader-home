from reader import domain, models


def get_page_path(*, comic: models.FileItem, page_number: int) -> str:
    cb_file = domain.get_cb_file_for_comic(comic)
    extract_path = domain.get_extract_path_for_comic(comic)
    return domain.get_comic_page_path(
        cb_file=cb_file,
        extract_path=extract_path,
        page_number=page_number,
    )
