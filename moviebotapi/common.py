from typing import Optional, Dict

from moviebotapi import Session


class CommonApi:
    def __init__(self, session: Session):
        self._session: Session = session

    def restart_app(self, secs: Optional[int] = 3):
        self._session.get('common.restart_app', {
            'secs': secs
        })

    def get_cache(self, namespace: str, key: str) -> Dict:
        return self._session.get('common.get_cache', {
            'namespace': namespace,
            'key': key
        })

    def set_cache(self, namespace: str, key: str, data: Dict):
        self._session.post('common.set_cache', {
            'namespace': namespace,
            'key': key,
            'data': data
        })
