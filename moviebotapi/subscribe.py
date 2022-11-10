import datetime
from enum import Enum
from typing import Dict, Optional

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
    def __init__(self, data: Dict, api: 'SubscribeApi'):
        self._api = api
        self.id: int = utils.parse_value(int, data.get('id'))
        self.uid: int = utils.parse_value(int, data.get('uid'))
        self.en_name: str = utils.parse_value(str, data.get('en_name'))
        self.desc: str = utils.parse_value(str, data.get('desc'))
        self.rating: float = utils.parse_value(float, data.get('rating'))
        self.status: SubStatus = utils.parse_value(SubStatus, data.get('status'))
        self.from_action: str = utils.parse_value(str, data.get('from_action'))
        self.alias: str = utils.parse_value(str, data.get('alias'))
        self.poster_path: str = utils.parse_value(str, data.get('poster_path'))
        self.download_mode: int = utils.parse_value(int, data.get('download_mode'))
        self.season_number: int = utils.parse_value(int, data.get('season_index'))
        self.episode_count: int = utils.parse_value(int, data.get('episode_count'))
        self.release_year: int = utils.parse_value(int, data.get('release_year'))
        self.season_year: int = utils.parse_value(int, data.get('season_year'))
        self.remote_search: bool = utils.parse_value(bool, data.get('remote_search'))
        self.is_aired: bool = utils.parse_value(bool, data.get('is_aired'))
        self.media_type: MediaType = utils.parse_value(MediaType, data.get('type'))
        self.thumb_image_path: str = utils.parse_value(str, data.get('thumb_image_path'))
        self.douban_id: int = utils.parse_value(int, data.get('douban_id'))
        self.tmdb_id: int = utils.parse_value(int, data.get('tmdb_id'))
        self.imdb_id: str = utils.parse_value(str, data.get('imdb_id'))
        self.genres: str = utils.parse_value(str, data.get('genres'))
        self.area: str = utils.parse_value(str, data.get('area'))
        self.choose_rule_name: str = utils.parse_value(str, data.get('choose_rule_name'))
        self.release_date: str = utils.parse_value(str, data.get('release_date'))
        self.cn_name: str = utils.parse_value(str, data.get('cn_name'))
        self.priority_keywords: str = utils.parse_value(str, data.get('priority_keywords'))
        self.filter_config: Dict = utils.parse_value(Dict, data.get('filter_config'))
        self.gmt_create: datetime.datetime = utils.parse_value(datetime.datetime, data.get('gmt_create'))
        self.gmt_modified: datetime.datetime = utils.parse_value(datetime.datetime, data.get('gmt_modified'))

    def delete(self, deep_delete: bool = False):
        self._api.delete(self.id, deep_delete)


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
