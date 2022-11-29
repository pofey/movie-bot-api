from typing import Dict

from moviebotapi import Session


class AuthApi:
    def __init__(self, session: Session):
        self._session: Session = session

    def get_default_ak(self, ) -> Dict:
        return self._session.get('auth.get_default_ak')
