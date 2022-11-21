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


class SearchResultItem:
    adult: bool
    backdrop_path: str
    genre_ids: List[int]
    id: int
    media_type: MediaType
    original_language: str
    original_title: str
    overview: str
    popularity: float
    poster_path: str
    release_date: str
    title: str
    video: bool
    vote_average: float
    vote_count: int

    def __init__(self, data: Dict):
        utils.copy_value(data, self)
        if 'first_air_date' in data:
            self.release_date = utils.parse_value(str, data.get('first_air_date'))
        else:
            self.release_date = utils.parse_value(str, data.get('release_date'))


class SearchResult:
    page: int
    total_pages: int
    total_results: int
    results: List[Union[SearchResultItem, "TmdbPerson"]]

    def __init__(self, data: Dict):
        self.page = utils.parse_value(int, data.get('page'))
        self.total_pages = utils.parse_value(int, data.get('total_pages'))
        self.total_results = utils.parse_value(int, data.get('total_results'))
        if data.get('results'):
            res = []
            for item in data.get('results'):
                if item.get('media_type') == 'person':
                    res.append(TmdbPerson(item))
                else:
                    res.append(SearchResultItem(item))
            self.results = res
        else:
            self.results = []


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


class TmdbPerson:
    adult: bool
    gender: int
    id: int
    known_for: List[SearchResultItem]
    known_for_department: str
    name: str
    popularity: float
    profile_path: str

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

    def search(self, media_type: MediaType, query: str, year: Optional[int] = None, language: Optional[str] = None):
        res = self._session.get('tmdb.search', {
            'media_type': media_type.value,
            'query': query,
            'language': language,
            'year': year
        })
        if not res:
            return
        result = []
        for item in res:
            item['media_type'] = media_type.value
            result.append(SearchResultItem(item))
        return result

    def search_multi(self, query: str, language: Optional[str] = None, page: Optional[int] = None) -> Optional[
        SearchResult]:
        res = self._session.get('tmdb.search_multi', {
            'query': query,
            'language': language,
            'page': page
        })
        if not res:
            return
        return SearchResult(res)
