from typing import Optional, Dict

from moviebotapi import Session
from moviebotapi.core import utils
from moviebotapi.core.models import MediaType
from moviebotapi.core.utils import json_object


@json_object
class MediaImage:
    """影片图片资源"""
    source: str
    banner: str
    poster: str
    small_poster: str
    clear_logo: str
    background: str
    small_backdrop: str
    thumb: str
    main_background: str
    main_poster: str

    def __init__(self, data: Dict):
        utils.copy_value(data, self)


class ScraperApi:
    def __init__(self, session: Session):
        self._session: Session = session

    def get_images(self, media_type: MediaType, tmdb_id: int, season_number: Optional[int] = None,
                   episode_number: Optional[int] = None) -> Optional[MediaImage]:
        data = self._session.get('scraper.get_media_image', {
            'media_type': media_type.value,
            'tmdb_id': tmdb_id,
            'season_number': season_number,
            'episode_number': episode_number
        })
        if not data:
            return
        return MediaImage(data)
