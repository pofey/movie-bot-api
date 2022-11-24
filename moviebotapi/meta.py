import datetime
from typing import Dict, Optional, List, Union

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


class Season:
    name: str
    season_number: int
    episode_count: int
    intro: str
    air_date: int
    poster_url: str
    douban_id: int

    def __init__(self, data: Dict):
        utils.copy_value(data, self, True)


class MediaMeta:
    id: int
    douban_id: int
    tmdb_id: int
    imdb_id: str
    tvdb_id: int
    # 数据最后更新时间
    gmt_modified: datetime.datetime
    media_type: MediaType
    title: str
    en_title: str
    original_title: str
    intro: str
    rating: float
    release_year: int
    # 首映日期
    premiere_date: int
    # 影片时常，单位分钟
    duration: int
    # 封面图
    poster_url: str
    # 背景图
    background_url: str
    genres: List[str]
    country: List[str]
    # 剧集时包含
    season_list: List[Season]

    def __init__(self, data: Dict):
        utils.copy_value(data, self, True)


class MetaApi:
    """
    自建数据操作接口
    请勿恶意调用，识别到违规刷数据行为直接封禁License
    """

    def __init__(self, session: Session):
        self._session: Session = session

    def get_cast_crew_by_douban(self, media_type: MediaType, douban_id: int):
        """
        根据豆瓣编号获取影片全部演员信息
        """
        list_ = self._session.get('meta.get_cast_crew_by_douban', {
            'media_type': media_type.value,
            'douban_id': douban_id
        })
        if not list_:
            return
        return [Person(x) for x in list_]

    def get_cast_crew_by_tmdb(self, media_type: MediaType, tmdb_id: int, season_number: Optional[int] = None) -> \
            Optional[List[Person]]:
        """
        根据tmdb信息获取影片全部演员信息
        """
        list_ = self._session.get('meta.get_cast_crew_by_tmdb', {
            'media_type': media_type.value,
            'tmdb_id': tmdb_id,
            'season_number': season_number
        })
        if not list_:
            return
        return [Person(x) for x in list_]

    def get_media_by_tmdb(self, media_type: MediaType, tmdb_id: int) -> Optional[Union[MediaMeta]]:
        """
        根据tmdb编号获取自建影视元数据
        """
        res = self._session.get('meta.get_media_by_tmdb_id', {
            'media_type': media_type.value,
            'tmdb_id': tmdb_id
        })
        if not res:
            return
        return MediaMeta(res)

    def get_media_by_douban(self, media_type: MediaType, tmdb_id: int):
        """
        根据豆瓣编号获取自建影视元数据
        """
        res = self._session.get('meta.get_media_by_douban_id', {
            'media_type': media_type.value,
            'douban_id': tmdb_id
        })
        if not res:
            return
        return MediaMeta(res)
