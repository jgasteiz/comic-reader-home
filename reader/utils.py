import logging
import os
from zipfile import ZipFile

from django.conf import settings
from django.http import Http404
from django.urls import reverse
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from rarfile import RarFile

from reader.models import Bookmark


class Utils(object):
    @staticmethod
    def get_encoded_path(decoded_path):
        return urlsafe_base64_encode(bytes(decoded_path, 'utf-8')).decode('utf-8').replace('\n', '')

    @staticmethod
    def get_decoded_path(encoded_path):
        return urlsafe_base64_decode(bytes(encoded_path, 'utf-8')).decode('utf-8')

    @staticmethod
    def clear_tmp():
        """
        Clear the tmp directory.
        """
        os.system('rm -rf {}/*'.format(settings.COMIC_EXTRACT_PATH))

    @staticmethod
    def extract_everything():
        """
        Extract every comic in the comic directory.
        """
        root_directory = Directory(None)
        root_directory.extract_recursively()


class PathBasedClass(object):
    def __init__(self, path):
        self.path = path
        self.utils = Utils()
        self.decoded_path = self.utils.get_decoded_path(path) if path is not None else settings.COMICS_ROOT

    def get_parent_path_url(self):
        """
        Given a path (string), build and return a directory_detail url of its parent.
        """
        parent_path = self.decoded_path.split('/')[:-1]
        parent_path = '/'.join(parent_path)
        parent_path = self.utils.get_encoded_path(parent_path)
        parent_path_url = reverse('reader:directory_detail', kwargs={'directory_path': parent_path})
        return parent_path_url


class Directory(PathBasedClass):
    def __init__(self, *args, **kwargs):
        super(Directory, self).__init__(*args, **kwargs)

        # Check whether the directory is root or not.
        self.is_root = self.decoded_path.lower().strip('/') == settings.COMICS_ROOT.lower().strip('/')
        # Get the parent path if the directory is not root.
        self.parent_path = self.get_parent_path_url() if not self.is_root else None
        # Set the directory name
        self.name = self.decoded_path.split('/')[-1]

    @property
    def listdir(self):
        return os.listdir(self.decoded_path)

    def get_child_abs_path(self, child_path):
        return os.path.join(self.decoded_path, child_path)

    def get_details(self, include_bookmarks):
        """
        For a given directory path:
        - get the comic files in that path
        - get the children directory paths in that path.
        """
        path_comics = []
        for comic_file_name in os.listdir(self.decoded_path):
            if not self.is_file_name_comic_file(comic_file_name):
                continue
            encoded_comic_file_path = self.get_comic_encoded_path(comic_file_name)

            comic = {
                'name': comic_file_name,
                'path': encoded_comic_file_path,
            }

            if include_bookmarks:
                qs = Bookmark.objects.filter(comic_path=encoded_comic_file_path)
                if qs.exists():
                    comic['bookmark'] = qs[0]

            path_comics.append(comic)

        # Build the path info object
        path_contents = {
            'name': self.name,
            'comics': path_comics,
            'directories': []
        }
        # Get all the children directories and their info.
        for path_name in self.listdir:
            child_path = self.get_child_abs_path(path_name)

            # Ignore it if the child name is in IGNORED FILE NAMES or if it's
            # not a directory.
            if any([
                path_name in settings.IGNORED_FILE_NAMES,
                not os.path.isdir(child_path)
            ]):
                continue

            path_contents['directories'].append({
                'name': path_name,
                'path': self.utils.get_encoded_path(child_path),
            })

        # Sort the comic names and child path names by name.
        path_contents['comics'] = sorted(path_contents['comics'], key=lambda x: x['name'])
        path_contents['directories'] = sorted(path_contents['directories'], key=lambda x: x['name'])

        return {
            'path_contents': path_contents,
            'is_root': self.is_root,
            'directory_path': self.path,
            'parent_path': self.parent_path
        }

    def extract_recursively(self):
        for path_name in self.listdir:
            child_path = self.get_child_abs_path(path_name)

            # Ignore it if the child name is in IGNORED FILE NAMES or if it's
            # not a directory.
            if path_name in settings.IGNORED_FILE_NAMES:
                continue

            # If the path is a directory, RECURSION!
            if os.path.isdir(child_path):
                directory = Directory(self.utils.get_encoded_path(child_path))
                directory.extract_recursively()
            # Otherwise, try to extract the comic.
            elif self.is_file_name_comic_file(path_name):
                comic = Comic(self.get_comic_encoded_path(path_name))
                print(u'Extracting {}'.format(comic.name))
                comic.extract_all_pages()

    @staticmethod
    def is_file_name_comic_file(file_name):
        if not file_name.endswith('.cbz') and not file_name.endswith('.cbr'):
            return False
        if file_name.startswith('.'):
            return False
        return True

    def get_comic_encoded_path(self, comic_file_name):
        comic_file_path = os.path.join(self.decoded_path, comic_file_name)
        encoded_comic_file_path = self.utils.get_encoded_path(comic_file_path)
        return encoded_comic_file_path.replace('\n', '')


class Comic(PathBasedClass):
    def __init__(self, *args, **kwargs):
        super(Comic, self).__init__(*args, **kwargs)

        self.name = self.decoded_path.split('/')[-1]
        self.extract_path = os.path.join(settings.COMIC_EXTRACT_PATH, self.utils.get_encoded_path(self.path))

        # Initialise the cb_file. This will raise a FileNotFoundError if
        # zipfile/rarfile can't find the file.
        if self.decoded_path.endswith('.cbz'):
            self.cb_file = ZipFile(self.decoded_path)
        else:
            self.cb_file = RarFile(self.decoded_path)

        # Set all the page names in order
        self.all_pages = sorted([
            p for p in self.cb_file.namelist()
            if p.endswith('.jpg') or p.endswith('.jpeg') or p.endswith('.png')
        ])

    def __len__(self):
        return len(self.all_pages)

    def __getitem__(self, position):
        return self.all_pages[position]

    def get_extracted_comic_page(self, page_number):
        """
        Extract the given page number or do nothing if it has been extracted already.
        """
        try:
            page_file_name = self[page_number]
        except IndexError:
            raise Http404

        page_file_path = os.path.join(self.extract_path, page_file_name)

        # If it exists already, return it.
        if os.path.exists(page_file_path):
            logging.info('Page exists, no need to extract it.')
            return page_file_path.replace(settings.BASE_DIR, '')

        # Need to make sure we create the extract path because
        # linux unrar-free won't create it if it doesn't exist.
        if not os.path.exists(self.extract_path):
            os.mkdir(self.extract_path)

        # Extract the actual page.
        self.cb_file.extract(page_file_name, self.extract_path)

        # And if it exists, return it.
        if os.path.exists(page_file_path):
            logging.info('Page extracted')
            return page_file_path.replace(settings.BASE_DIR, '')

        # Otherwise something went wrong, raise 404.
        raise Http404

    def extract_all_pages(self):
        if not os.path.exists(self.extract_path):
            os.mkdir(self.extract_path)
            self.cb_file.extractall(self.extract_path)

    def bookmark_page(self, page_number):
        """
        Create a bookmark on the given page or update an existing one
        for this comic with the given page.
        """
        bookmark, created = Bookmark.objects.get_or_create(
            comic_path=self.path,
            title=self.name
        )
        bookmark.page_num = page_number
        bookmark.save()
