from typing import List, Dict, Optional

from moviebotapi import Session
from moviebotapi.core import utils


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


class AmrApi:
    """
    Automatic media Recognition
    自动媒体信息分析接口
    """

    def __init__(self, session: Session):
        self._session: Session = session

    def parse_name_meta_by_string(self, string: str) -> Optional[MediaNameMeta]:
        res = self._session.get('amr.parse_name_meta_by_string', {
            'string': string
        })
        if not res:
            return
        return MediaNameMeta(res)

    def parse_name_meta_by_filepath(self, filepath: str) -> Optional[MediaNameMeta]:
        res = self._session.get('amr.parse_name_meta_by_filepath', {
            'filepath': filepath
        })
        if not res:
            return
        return MediaNameMeta(res)
