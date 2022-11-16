from typing import Dict, Optional, List

from moviebotapi import Session
from moviebotapi.core import utils
from moviebotapi.core.models import MediaType


class Person:
    id: int
    douban_id: int
    imdb_id: str
    cn_name: str
    en_name: str
    aka_cn_names: str
    aka_en_names: str
    country: str
    date_of_birth: str
    douban_image_url: str
    description: str
    role: str
    duty: str
    order_number: int

    def __init__(self, data: Dict):
        utils.copy_value(data, self, True)


class MetaApi:
    def __init__(self, session: Session):
        self._session: Session = session

    def get_cast_crew_by_douban(self, media_type: MediaType, douban_id: int):
        list_ = self._session.get('meta.get_cast_crew_by_douban', {
            'media_type': media_type.value,
            'douban_id': douban_id
        })
        if not list_:
            return
        return [Person(x) for x in list_]

    def get_cast_crew_by_tmdb(self, media_type: MediaType, tmdb_id: int, season_number: Optional[int] = None) -> \
            Optional[List[Person]]:
        list_ = self._session.get('meta.get_cast_crew_by_tmdb', {
            'media_type': media_type.value,
            'tmdb_id': tmdb_id,
            'season_number': season_number
        })
        if not list_:
            return
        return [Person(x) for x in list_]
