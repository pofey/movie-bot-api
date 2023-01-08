from typing import Optional, Dict, List

from moviebotapi import Session
from moviebotapi.core import utils
from moviebotapi.core.utils import json_object


@json_object
class MenuSubItem:
    href: str
    icon: str
    title: str

    def __init__(self, data: Dict = None):
        if data:
            utils.copy_value(data, self)


@json_object
class MenuItem:
    href: str
    """
    icon的值就是MUI icon的名称
    https://mui.com/material-ui/material-icons/
    """
    icon: str
    title: str
    children: List[MenuSubItem]

    def __init__(self, data: Dict = None):
        if data:
            utils.copy_value(data, self)


@json_object
class MenuGroup:
    title: str
    pages: List[MenuItem]

    def __init__(self, data: Dict):
        utils.copy_value(data, self)


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

    def get_image_text(self, b64_img: str):
        return self._session.post('common.get_image_text', {
            'b64_image': b64_img
        })

    def get_cache_image_filepath(self, img_url: str) -> str:
        return self._session.get('common.get_cache_image_filepath', {
            'url': img_url
        })

    def list_menus(self) -> List[MenuGroup]:
        items = self._session.get('common.get_menus')
        if not items:
            return []
        return [MenuGroup(x) for x in items]

    def save_menus(self, menus: List[MenuGroup]):
        if not menus:
            return
        self._session.post('common.save_menus', {
            'menus': [x.to_json() for x in menus]
        })
