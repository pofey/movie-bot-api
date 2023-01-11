from enum import Enum
from typing import List, Optional, Dict

from moviebotapi import Session
from moviebotapi.core import utils
from moviebotapi.core.models import MediaType
from moviebotapi.core.utils import json_object


@json_object
class MediaLibraryPath:
    path: str
    auto_scan: bool = False

    def __init__(self, data: Dict = None):
        if not data:
            utils.copy_value(data, self)


@json_object
class TransferMode(Enum):
    HardLink = 'link'
    Copy = 'copy'
    Move = 'move'


class LibraryApi:
    def __init__(self, session: Session):
        self._session: Session = session

    def start_scanner(self, library_id: int):
        self._session.get('library.start_scanner', {
            'library_id': library_id
        })

    def stop_scanner(self, library_id: int):
        self._session.get('library.stop_scanner', {
            'library_id': library_id
        })

    def add_library(self, media_type: MediaType, library_name: str, library_paths: List[MediaLibraryPath]) -> Optional[
        int]:
        return self._session.post('library.add_library', {
            'library_name': library_name,
            'media_type': media_type.value,
            'library_paths': [utils.to_dict(x) for x in library_paths]
        })

    def rename_by_path(self, path: str):
        return self._session.post('library.rename_by_path', {
            'path': path
        })

    def direct_transfer(self, src: str, dst: str, mode: TransferMode):
        self._session.post('library.direct_transfer', {
            'src': src,
            'dst': dst,
            'mode': mode.value
        })
