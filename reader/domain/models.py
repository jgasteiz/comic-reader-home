import dataclasses
import enum
from typing import List, Optional


class FileType(enum.Enum):
    COMIC = "comic"
    DIRECTORY = "directory"


@dataclasses.dataclass(frozen=True)
class FileItem:
    id: int
    name: str
    path: str
    file_type: FileType
    parent: Optional["FileItem"]
    furthest_read_page: int
    is_read: bool
    is_favorite: bool

    def is_comic(self) -> bool:
        return self.file_type == FileType.COMIC

    def is_directory(self) -> bool:
        return self.file_type == FileType.DIRECTORY


@dataclasses.dataclass(frozen=True)
class DirectoryDetails:
    file_items: List[FileItem]
    parent: Optional[FileItem]
