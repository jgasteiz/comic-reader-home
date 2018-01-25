import base64
import logging
import os

from django.conf import settings

from reader.models import Bookmark


class PageNotFoundError(Exception):
    pass


def clear_tmp():
    """
    Clear the tmp directory.
    """
    if os.name != 'nt':
        os.system('rm -rf {}/*'.format(settings.COMIC_TMP_PATH))
    else:
        os.system('del /s /q "{}"'.format(settings.COMIC_TMP_PATH))


def extract_comic_page(cb_file, page_number, comic_path):
    """
    Extract the given page for the given comic file or do nothing if it's
    in place alreday.
    """
    page_file_name = get_comic_page_name(cb_file, page_number)
    page_file_path = os.path.join(settings.COMIC_TMP_PATH, page_file_name)

    # If it exists already, return it.
    if os.path.exists(page_file_path):
        logging.info('Page exists, returning its path')
        return page_file_path

    # Otherwise extract it.
    if os.name != 'nt':
        cb_file.extract(page_file_name, settings.COMIC_TMP_PATH)
    else:
        if comic_path.endswith('.cbz'):
            cb_file.extract(page_file_name, settings.COMIC_TMP_PATH)
        else:
            command = 'unrar x /y "{cbr_path}" "{page_name}"'.format(
                cbr_path=comic_path,
                page_name=page_file_name.replace('/', '\\'),
            )
            logging.info(command)
            os.system(command)

    # And if it exists, return it.
    if os.path.exists(page_file_path):
        logging.info('PAGE EXTRACTED')
        return page_file_path

    # Otherwise something went wrong, return None.
    raise PageNotFoundError


def get_all_comic_pages(cb_file):
    return [p for p in cb_file.namelist()
            if p.endswith('.jpg') or p.endswith('.png') or p.endswith('.webp')]


def get_num_comic_pages(cb_file):
    return len(get_all_comic_pages(cb_file))


def get_comic_page_name(cb_file, page_number):
    """
    Get the given cb_file page file name in the page_number position.
    """
    all_pages = sorted(get_all_comic_pages(cb_file))
    try:
        return all_pages[page_number]
    except IndexError:
        raise PageNotFoundError


def get_extracted_comic_page(cb_file, page_number, comic_path):
    """
    Extract a page from the given cb file given its page number
    """
    try:
        page_file_path = extract_comic_page(cb_file=cb_file, page_number=page_number, comic_path=comic_path)
        return page_file_path.replace(settings.BASE_DIR, '')
    except PageNotFoundError:
        return settings.PAGE_NOT_FOUND


def get_directory_details(directory_path=None):
    """
    For a given directory path:
    - get the comic files in that path
    - get the children directory paths in that path.
    """
    if directory_path:
        decoded_directory_path = base64.decodebytes(bytes(directory_path, 'utf-8')).decode('utf-8')
    else:
        decoded_directory_path = settings.COMICS_ROOT

    directory_name = decoded_directory_path.split('/')[-1]

    # Get the path comic files
    path_comics = []
    for comic_file_name in os.listdir(decoded_directory_path):
        if not comic_file_name.endswith('.cbz') and not comic_file_name.endswith('.cbr'):
            continue
        if comic_file_name.startswith('.'):
            continue
        comic_file_path = os.path.join(decoded_directory_path, comic_file_name)
        comic_file_path = base64.encodebytes(bytes(comic_file_path, 'utf-8')).decode('utf-8')
        comic_file_path = comic_file_path.replace('\n', '')
        bookmark = None
        qs = Bookmark.objects.filter(comic_path=comic_file_path)
        if qs.exists():
            bookmark = qs[0]
        path_comics.append({
            'name': comic_file_name,
            'path': comic_file_path,
            'bookmark': bookmark,
        })

    # Build the path info object
    path_contents = {
        'name': directory_name,
        'comics': path_comics,
        'directories': []
    }
    # Per directory in the current path, get their path info.
    for path_name in os.listdir(decoded_directory_path):
        child_path = os.path.join(decoded_directory_path, path_name)

        # Ignore it if the child name is in IGNORED FILE NAMES or if it's
        # not a directory.
        if any([
            path_name in settings.IGNORED_FILE_NAMES,
            not os.path.isdir(child_path)
        ]):
            continue

        path_contents['directories'].append({
            'name': path_name,
            'path': base64.encodebytes(bytes(child_path, 'utf-8')).decode('utf-8').replace('\n', ''),
        })

    # Sort the comic names and child path names by name.
    path_contents['comics'] = sorted(path_contents['comics'], key=lambda x: x['name'])
    path_contents['directories'] = sorted(path_contents['directories'], key=lambda x: x['name'])

    return {
        'path_contents': path_contents,
        'is_root': decoded_directory_path == settings.COMICS_ROOT,
        'directory_path': directory_path
    }
