from typing import List, Dict, Optional

from moviebotapi import Session
from moviebotapi.core import utils
from moviebotapi.core.models import MediaType
from moviebotapi.core.utils import json_object


@json_object
class MediaNameMeta:
    cn_name: str = None
    aka_names: List[str] = []
    en_name: str = None
    year: int = None
    season_number: List[int] = None
    episode_number: List[int] = None
    resolution: str = None
    media_source: str = None
    media_codec: str = None
    media_audio: List[str] = None
    release_team: str = None

    def __init__(self, data: Dict):
        utils.copy_value(data, self)


@json_object
class MetaSearchResult:
    tmdb_id: int = None
    douban_id: int = None
    cn_name: str = None
    original_name: str = None
    release_year: int = None
    release_date: str = None
    media_type: MediaType = None
    season_number: int = None

    def __init__(self, data: Dict):
        utils.copy_value(data, self)


class AmrApi:
    """
    Automatic media Recognition
    自动媒体信息分析接口
    """

    def __init__(self, session: Session):
        self._session: Session = session

    def parse_name_meta_by_string(self, string: str) -> Optional[MediaNameMeta]:
        """
        根据一个字符串（种子名、文件名等）解析出名称中包含的影片信息
        """
        res = self._session.get('amr.parse_name_meta_by_string', {
            'string': string
        })
        if not res:
            return
        return MediaNameMeta(res)

    def parse_name_meta_by_filepath(self, filepath: str) -> Optional[MediaNameMeta]:
        """
        根据一个影片文件路径解析出影片信息
        需要为完整路径，会根据分析上级目录的有效信息进行解析
        """
        res = self._session.get('amr.parse_name_meta_by_filepath', {
            'filepath': filepath
        })
        if not res:
            return
        return MediaNameMeta(res)

    def analysis_string(self, string: str):
        """
        根据一个字符串（种子名、文件名等），分析出它对应的影片信息，包括TMDBID
        """
        res = self._session.get('amr.analysis_string', {
            'string': string
        })
        if not res:
            return
        return MetaSearchResult(res)

    def analysis_filepath(self, filepath: str):
        """
        根据一个影片文件路径，分析出它对应的影片信息，包括TMDBID
        """
        res = self._session.get('amr.analysis_filepath', {
            'string': filepath
        })
        if not res:
            return
        return MetaSearchResult(res)

    def analysis_douban_meta(self, cn_name: Optional[str], en_name: Optional[str] = None, year: Optional[int] = None,
                             season_number: Optional[int] = None):
        """
        根据提供的信息，分析出豆瓣的关联影片
        """
        res = self._session.get('amr.analysis_douban_meta', {
            'cn_name': cn_name,
            'en_name': en_name,
            'year': year,
            'season_number': season_number
        })
        if not res:
            return
        return MetaSearchResult(res)
