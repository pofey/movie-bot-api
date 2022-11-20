import datetime
from enum import Enum
from typing import Dict, Optional, List

from moviebotapi import Session
from moviebotapi.core import utils
from moviebotapi.core.models import MediaType


class SubStatus(int, Enum):
    """
    订阅中
    """
    Subscribing = 0
    """
    订阅已经完成
    """
    Completed = 1
    """
    等待更好的版本
    """
    WaitVersion = 2


class Subscribe:
    id: int
    uid: int
    en_name: str
    desc: str
    rating: float
    status: SubStatus
    from_action: str
    alias: str
    poster_path: str
    download_mode: int
    episode_count: int
    release_year: int
    season_year: int
    remote_search: bool
    is_aired: bool
    media_type: MediaType
    thumb_image_path: str
    douban_id: int
    tmdb_id: int
    imdb_id: str
    genres: str
    area: str
    choose_rule_name: str
    release_date: str
    cn_name: str
    priority_keywords: str
    filter_config: Dict
    gmt_create: datetime.datetime
    gmt_modified: datetime.datetime

    def __init__(self, data: Dict, api: 'SubscribeApi'):
        utils.copy_value(data, self)
        self._api = api
        self.season_number: int = utils.parse_value(int, data.get('season_index'))

    def delete(self, deep_delete: bool = False):
        self._api.delete(self.id, deep_delete)


class Filter:
    filter_name: str
    priority: int
    download_mode: int
    apply_media_type: List[MediaType]
    apply_genres: List[str]
    apply_country: List[str]
    apply_min_year: int
    apply_max_year: int
    media_source: List[str]
    resolution: List[str]
    media_codes: List[str]
    has_cn: bool
    has_special: bool
    min_size: int
    max_size: int
    min_seeders: int
    max_seeders: int
    free_only: bool
    pass_hr: bool
    exclude_keyword: str
    include_keyword: str

    def __init__(self, data: Dict, api: 'SubscribeApi'):
        utils.copy_value(data, self)
        self._api = api
        self.apply_genres = utils.parse_value(List[str], data.get('apply_cate'))
        self.apply_country = utils.parse_value(List[str], data.get('apply_area'))


class SubscribeApi:
    def __init__(self, session: Session):
        self._session: Session = session

    def get(self, subscribe_id: int) -> Optional[Subscribe]:
        sub = self._session.get('subscribe.get_sub', params={'id': subscribe_id})
        if not sub:
            return
        return Subscribe(sub, self)

    def list(self, media_type: Optional[MediaType] = None, status: Optional[SubStatus] = None):
        params = {}
        if media_type:
            params.update({'media_type': media_type.value})
        if status is not None:
            params.update({'status': status.value})
        list_ = self._session.get('subscribe.list', params=params)
        if not list_:
            return []
        return [Subscribe(x, self) for x in list_]

    def delete(self, subscribe_id: int, deep_delete: bool = False):
        self._session.post('subscribe.delete_sub', json={
            'id': subscribe_id,
            'deep_delete': deep_delete
        })

    def sub_by_tmdb(self, media_type: MediaType, tmdb_id: int, season_number: Optional[int] = None):
        params = {}
        if media_type:
            params.update({'media_type': media_type.value})
        if tmdb_id:
            params.update({'tmdb_id': tmdb_id})
        if season_number is not None:
            params.update({'season_number': season_number})
        self._session.get('subscribe.sub_tmdb', params=params)

    def sub_by_douban(self, douban_id: int, filter_name: Optional[str] = None):
        params = {'id': douban_id}
        if filter_name:
            params.update({'filter_name': filter_name})
        self._session.get('subscribe.sub_douban', params=params)

    def get_filters(self):
        list_ = self._session.get('subscribe.get_filters')
        if not list_:
            return []
        return [Filter(x, self) for x in list_]
