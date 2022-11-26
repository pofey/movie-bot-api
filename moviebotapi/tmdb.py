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
        if 'original_name' in data:
            self.original_title = utils.parse_value(str, data.get('original_name'))
        else:
            self.original_title = utils.parse_value(str, data.get('original_title'))
        if 'title' in data:
            self.title = utils.parse_value(str, data.get('title'))
        else:
            self.title = utils.parse_value(str, data.get('name'))


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


class TmdbPerson:
    adult: bool
    gender: int
    id: int
    known_for: List[SearchResultItem]
    known_for_department: str
    name: str
    original_name: str
    popularity: float
    profile_path: str
    credit_id: str
    department: str
    job: str
    character: str
    order: int

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
    crew: List[TmdbPerson]
    guest_stars: List[TmdbPerson]

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


class TmdbCredits:
    id: int
    cast: List[TmdbPerson]
    crew: List[TmdbPerson]

    def __init__(self, data: Dict):
        utils.copy_value(data, self)


class TmdbAkaName:
    iso_3166_1: str
    title: str

    def __init__(self, data: Dict):
        utils.copy_value(data, self)


class TmdbExternalIds:
    id: int
    imdb_id: str
    wikidata_id: str
    facebook_id: str
    instagram_id: str
    twitter_id: str

    def __init__(self, data: Dict):
        utils.copy_value(data, self)


class TmdbApi:
    def __init__(self, session: Session):
        self._session: Session = session

    def get(self, media_type: MediaType, tmdb_id: int, language: Optional[str] = None) -> Union[
        TmdbMovie, TmdbTV, None]:
        """
        根据编号获取详情
        """
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

    def get_external_ids(self, media_type: MediaType, tmdb_id: int):
        """
        根据tmdb id获取其他媒体平台的id
        """
        res = self._session.get('tmdb.get_external_ids', {
            'media_type': media_type.value,
            'tmdb_id': tmdb_id
        })
        if not res:
            return
        return TmdbExternalIds(res)

    def get_credits(self, media_type: MediaType, tmdb_id: int, season_number: Optional[int] = None):
        """
        获取演员，剧组成员信息
        """
        res = self._session.get('tmdb.get_credits', {
            'media_type': media_type.value,
            'tmdb_id': tmdb_id,
            'season_number': season_number
        })
        if not res:
            return
        return TmdbCredits(res)

    def search(self, media_type: MediaType, query: str, year: Optional[int] = None, language: Optional[str] = None):
        """
        根据特定的媒体类型搜索
        """
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
        """
        混合搜索，电影、剧集、演员都搜
        """
        res = self._session.get('tmdb.search_multi', {
            'query': query,
            'language': language,
            'page': page
        })
        if not res:
            return
        return SearchResult(res)

    def get_aka_names(self, media_type: MediaType, tmdb_id: int) -> List[TmdbAkaName]:
        list_ = self._session.get('tmdb.get_aka_names', {
            'media_type': media_type.value,
            'tmdb_id': tmdb_id
        })
        if not list_:
            return []
        return [TmdbAkaName(x) for x in list_]

    def get_tv_episode(self, tmdb_id: int, season_number: int, episode_number: int, language: Optional[str] = None) -> \
    Optional[EpisodeMeta]:
        res = self._session.get('tmdb.get_tv_episode', {
            'tmdb_id': tmdb_id,
            'season_number': season_number,
            'episode_number': episode_number,
            'language': language
        })
        if not res:
            return
        return EpisodeMeta(res)
