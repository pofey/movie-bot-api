from typing import Optional, List, Dict, Union

from moviebotapi import Session
from moviebotapi.core import utils
from moviebotapi.core.decorators import ignore_attr_not_exists
from moviebotapi.core.models import MediaType


class TmdbGenres:
    id: int
    name: str

    def __init__(self, data: Dict):
        utils.copy_value(data, self)


class ProductionCompanies:
    id: int
    logo_path: str
    name: str
    origin_country: str

    def __init__(self, data: Dict):
        utils.copy_value(data, self)


class SpokenLanguages:
    english_name: str
    iso_639_1: str
    name: str

    def __init__(self, data: Dict):
        utils.copy_value(data, self)


@ignore_attr_not_exists
class TmdbMovie:
    id: int
    imdb_id: str
    adult: bool
    backdrop_path: str
    belongs_to_collection: str
    budget: int
    genres: List[TmdbGenres]
    homepage: str
    original_language: str
    title: str
    original_title: str
    overview: str
    popularity: float
    poster_path: str
    release_date: str
    revenue: int
    runtime: int
    status: str
    tagline: str
    video: bool
    vote_average: float
    vote_count: int
    production_companies: List[ProductionCompanies]
    production_countries: List
    spoken_languages: List[SpokenLanguages]

    def __init__(self, data: Dict):
        utils.copy_value(data, self)


class EpisodeMeta:
    air_date: str
    episode_number: int
    id: int
    name: str
    overview: str
    production_code: str
    runtime: int
    season_number: int
    show_id: int
    still_path: str
    vote_average: float
    vote_count: int

    def __init__(self, data: Dict):
        utils.copy_value(data, self)


class Network:
    id: int
    name: str
    logo_path: str
    origin_country: str

    def __init__(self, data: Dict):
        utils.copy_value(data, self)


class Season:
    air_date: str
    episode_count: int
    id: int
    name: str
    overview: str
    poster_path: str
    season_number: int

    def __init__(self, data: Dict):
        utils.copy_value(data, self)


@ignore_attr_not_exists
class TmdbTV:
    name: str
    original_name: str
    id: int
    in_production: bool
    adult: bool
    backdrop_path: str
    first_air_date: str
    last_air_date: str
    episode_run_time: List[int]
    genres: List[TmdbGenres]
    homepage: str
    languages: List[str]
    number_of_episodes: int
    number_of_seasons: int
    origin_country: List[str]
    original_language: List[str]
    overview: str
    popularity: float
    poster_path: str
    production_companies: List[ProductionCompanies]
    production_countries: List
    spoken_languages: List[SpokenLanguages]
    status: str
    tagline: str
    type: str
    vote_average: float
    vote_count: int
    created_by: dict
    last_episode_to_air: EpisodeMeta
    next_episode_to_air: EpisodeMeta
    networks: List[Network]
    seasons: List[Season]

    def __init__(self, data: Dict):
        utils.copy_value(data, self)


class TmdbApi:
    def __init__(self, session: Session):
        self._session: Session = session

    def get(self, media_type: MediaType, tmdb_id: int, language: Optional[str] = None) -> Union[
        TmdbMovie, TmdbTV, None]:
        if not language:
            language = 'zh-CN'
        meta = self._session.get('tmdb.get', {
            'media_type': media_type.value,
            'tmdb_id': tmdb_id,
            'language': language
        })
        if not meta:
            return
        if media_type == MediaType.Movie:
            return TmdbMovie(meta)
        else:
            return TmdbTV(meta)
