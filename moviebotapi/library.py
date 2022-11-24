from typing import List

from moviebotapi import Session


class LibraryApi:
    def __init__(self, session: Session):
        self._session: Session = session

    def start_scanner(self, library_path: List[str]):
        self._session.post('library.start_scanner', {
            'library_path': library_path
        })

    def stop_scanner(self, library_path: List[str]):
        self._session.post('library.stop_scanner', {
            'library_path': library_path
        })
