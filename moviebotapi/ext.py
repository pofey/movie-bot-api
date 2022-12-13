from typing import Union, Optional, List

from moviebotapi.core import utils
from moviebotapi.core.models import MediaType
from moviebotapi.douban import DoubanMedia
from moviebotapi.tmdb import TmdbMovie, TmdbTV


class MediaMetaSelect:
    def __init__(self, douban: Optional[DoubanMedia] = None, tmdb: Optional[Union[TmdbMovie, TmdbTV]] = None):
        self.douban = douban
        self.tmdb = tmdb

    @property
    def country(self):
        country: List[str] = list()
        if self.tmdb:
            if hasattr(self.tmdb, 'production_countries') and not self.tmdb.production_countries and hasattr(self.tmdb,
                                                                                                             'origin_country') and not self.tmdb.origin_country:
                return ['其他']
            if hasattr(self.tmdb, 'origin_country') and self.tmdb.origin_country:
                for c in self.tmdb.origin_country:
                    country.append(utils.Countries.get(c))
            if len(country) == 0 and hasattr(self.tmdb, 'production_countries') and self.tmdb.production_countries:
                for c in self.tmdb.production_countries:
                    country.append(utils.Countries.get(c.get('iso_3166_1')))
        if not country and self.douban:
            country = self.douban.country
        return country

    @property
    def genres(self):
        genres = None
        if not genres and self.tmdb and self.tmdb.genres:
            arr = []
            for item in self.tmdb.genres:
                if item.name == 'Sci-Fi & Fantasy':
                    arr.append('科幻')
                elif item.name == 'War & Politics':
                    arr.append('战争')
                else:
                    arr.append(item.name)
            genres = arr
        if not genres and self.douban:
            genres = self.douban.genres
        return genres

    @property
    def episode_count(self):
        if self.douban and self.douban.episode_count:
            return self.douban.episode_count
        if self.tmdb and isinstance(self.tmdb, TmdbTV):
            return self.tmdb.number_of_episodes
        return 1

    @property
    def title(self):
        title = None
        if self.douban:
            if self.douban.media_type == MediaType.TV:
                title = utils.MediaParser.trim_season(self.douban.cn_name)
            else:
                title = self.douban.cn_name
            if title == '未知电视剧' or title == '未知电影':
                title = None
        if self.tmdb and not title:
            if isinstance(self.tmdb, TmdbMovie):
                title = self.tmdb.title
            elif isinstance(self.tmdb, TmdbTV):
                title = self.tmdb.name
        return title

    @property
    def rating(self):
        rating = None
        if self.douban:
            rating = self.douban.rating
        if not rating and self.tmdb:
            rating = self.tmdb.vote_average
        if rating:
            return round(rating, 1)
        else:
            return rating

    @property
    def url(self):
        if self.douban:
            return 'https://movie.douban.com/subject/%s/' % self.douban.id
        if self.tmdb:
            if isinstance(self.tmdb, TmdbMovie):
                return 'https://themoviedb.org/movie/%s' % self.tmdb.id
            else:
                return 'https://themoviedb.org/tv/%s' % self.tmdb.id
        return

    @property
    def intro(self):
        intro = None
        if self.douban:
            intro = self.douban.intro
        if self.tmdb and not intro:
            intro = self.tmdb.overview
        if intro:
            return str(intro).strip()
        else:
            return intro

    @staticmethod
    def _get_tmdb_tv_date(tv: TmdbTV) -> Optional[str]:
        if tv.first_air_date:
            return tv.first_air_date
        elif tv and tv.seasons and tv.seasons[0].air_date:
            return tv.seasons[0].air_date[0:4]
        return

    @property
    def release_year(self):
        if self.douban:
            return self.douban.release_year
        if self.tmdb:
            if isinstance(self.tmdb, TmdbMovie):
                if self.tmdb.release_date:
                    return self.tmdb.release_date[0:4]
                else:
                    return
            else:
                tv_data = self._get_tmdb_tv_date(self.tmdb)
                return tv_data[0:4] if tv_data else None

    @property
    def release_date(self):
        date = None
        if self.tmdb:
            if isinstance(self.tmdb, TmdbMovie):
                if self.tmdb.release_date:
                    date = self.tmdb.release_date
            else:
                date = self._get_tmdb_tv_date(self.tmdb)
        if self.douban and not date:
            date = self.douban.premiere_date
        return date
