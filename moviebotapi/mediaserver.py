from typing import List, Dict

from moviebotapi import Session
from moviebotapi.core import utils
from moviebotapi.core.models import MediaType
from moviebotapi.core.utils import json_object


@json_object
class SubtitleStream:
    """字幕流信息"""
    codec: str
    language: str
    display_language: str
    display_title: str
    # 外部字幕
    external: bool
    is_default: bool

    def __init__(self, data: Dict):
        utils.copy_value(data, self)


@json_object
class AudioStream:
    """音频流信息"""
    codec: str
    language: str
    display_language: str
    display_title: str
    is_default: bool
    channel_layout: str

    def __init__(self, data: Dict):
        utils.copy_value(data, self)


@json_object
class MediaItem:
    """媒体服务器的影片基础模型"""
    tmdb_id: int
    imdb_id: str
    tvdb_id: str
    url: str
    id: str
    name: str
    # 剧集才有，集号
    index: int
    type: MediaType
    poster_url: str
    thumb_url: str
    backdrop_url: str

    # 视频容器类型 mkv 原盘
    video_container: str
    # 视频编码
    video_codec: str
    # 视频分辨率
    video_resolution: str
    # 字幕流
    subtitle_streams: List[SubtitleStream]
    # 音频流
    audio_streams: List[AudioStream]
    sub_items: list
    # 播放状态
    status: int

    def __init__(self, data: Dict):
        utils.copy_value(data, self)


class MediaServerApi:
    def __init__(self, session: Session):
        self._session: Session = session

    def list_episodes_from_tmdb(self, tmdb_id: int, season_number: int, fetch_all: bool = False):
        items = self._session.get('media_server.list_episodes_from_tmdb', {
            'tmdb_id': tmdb_id,
            'season_number': season_number,
            'fetch_all': fetch_all
        })
        if not items:
            return []
        return [MediaItem(x) for x in items]

    def search_by_tmdb(self, tmdb_id: int, fetch_all: bool = False):
        items = self._session.get('media_server.search_by_tmdb', {
            'tmdb_id': tmdb_id,
            'fetch_all': fetch_all
        })
        if not items:
            return []
        return [MediaItem(x) for x in items]
