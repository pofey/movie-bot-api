from enum import Enum
from typing import Dict, List, Optional

from moviebotapi import Session
from moviebotapi.core import utils
from moviebotapi.core.models import MediaType
from moviebotapi.core.utils import json_object
from moviebotapi.subscribe import SubStatus


@json_object
class DoubanPeople:
    """剧组人员、导演、演员等人员信息"""
    douban_id: int
    tmdb_id: int
    imdb_id: str
    name: str
    en_name: str
    role: str
    pic_url: str
    type: str

    def __init__(self, data: Dict):
        utils.copy_value(data, self)


@json_object
class DoubanMedia:
    id: int
    url: str
    release_year: str
    local_name: str
    en_name: str
    cover_image: str
    rating: float
    user_id: str
    intro: str
    director: List[DoubanPeople]
    actor: List[DoubanPeople]
    duration: int
    trailer_video_url: str

    def __init__(self, data: Dict):
        utils.copy_value(data, self)
        # 对历史遗留接口不规范命名做更正
        self.media_type: MediaType = utils.parse_value(MediaType, data.get('type'))
        self.aka_names: List[str] = utils.parse_value(List[str], data.get('alias'))
        self.genres: List[str] = utils.parse_value(List[str], data.get('cates'))
        self.country: List[str] = utils.parse_value(List[str], data.get('area'))
        self.cn_name: str = utils.parse_value(str, data.get('name'))
        self.premiere_date: str = utils.parse_value(str, data.get('release_date'))
        self.imdb_id: str = utils.parse_value(str, data.get('imdb'))
        self.episode_count: int = utils.parse_value(int, data.get('total_ep_count'))
        self.season_index: int = utils.parse_value(int, data.get('season_index'))


@json_object
class DoubanSearchResult:
    id: int
    cn_name: str
    rating: float
    url: str
    app_url: str
    sub_id: int
    status: SubStatus

    def __init__(self, data: Dict):
        utils.copy_value(data, self)
        self.poster_url: str = utils.parse_value(str, data.get('poster_path'))


@json_object
class DoubanRankingType(Enum):
    movie_top250 = '豆瓣电影Top250'
    movie_real_time_hotest = '实时热门电影'
    movie_weekly_best = '一周口碑电影榜'
    ECPE465QY = '近期热门电影榜'
    EC7Q5H2QI = '近期高分电影榜'

    tv_chinese_best_weekly = '华语口碑剧集榜'
    tv_global_best_weekly = '全球口碑剧集榜'
    show_chinese_best_weekly = '国内口碑综艺榜'
    show_global_best_weekly = '国外口碑综艺榜'

    ECFA5DI7Q = '近期热门美剧'
    EC74443FY = '近期热门大陆剧'
    ECNA46YBA = '近期热门日剧'
    ECBE5CBEI = '近期热门韩剧'

    ECAYN54KI = '近期热门喜剧'
    ECBUOLQGY = '近期热门动作'
    ECSAOJFTA = '近期热门爱情'
    ECZYOJPLI = '近期热门科幻'
    EC3UOBDQY = '近期热门动画'
    ECPQOJP5Q = '近期热门悬疑'


@json_object
class DoubanRankingItem:
    rank: int
    id: int
    poster_path: str
    background_url: str
    cn_name: str
    release_year: str
    media_type: MediaType
    rating: float
    url: str
    app_url: str
    desc: str
    comment: str

    def __init__(self, data: Dict):
        utils.copy_value(data, self)
        self.media_type = MediaType.get(data.get('type'))


@json_object
class ApiSearchItem:
    media_type: MediaType
    douban_id: int
    rating: float
    title: str
    app_url: str
    small_poster_url: str
    year: int

    def __init__(self, data: Dict):
        if data.get('target_type'):
            self.media_type = MediaType.Movie if data.get('target_type') == 'movie' else MediaType.TV
        self.douban_id = utils.parse_value(int, data.get('target_id'))
        if data.get('target'):
            t = data.get('target')
            self.title = utils.parse_value(str, t.get('title'))
            self.app_url = utils.parse_value(str, t.get('uri'))
            self.small_poster_url = utils.parse_value(str, t.get('cover_url'))
            self.year = utils.parse_value(int, t.get('year'))
            self.rating = utils.parse_value(float, t.get('rating').get('value') if t.get('rating') else None)


@json_object
class DoubanDailyMedia:
    show_date: str
    media_type: str
    media_id: int
    douban_id: int
    tmdb_id: int
    title: str
    comment: str
    release_year: int
    rating: float
    poster_url: str
    background_url: str
    url: str
    app_url: str

    def __init__(self, data: Dict):
        utils.copy_value(data, self, True)


class DoubanApi:
    def __init__(self, session: Session):
        self._session: Session = session

    def get(self, douban_id: int) -> Optional[DoubanMedia]:
        """
        根据豆瓣编号获取豆瓣详情信息
        """
        meta = self._session.get('douban.get', {
            'douban_id': douban_id
        })
        if not meta:
            return
        return DoubanMedia(meta)

    def search(self, keyword: str) -> List[DoubanSearchResult]:
        """
        搜索豆瓣移动端网页解析结果，此搜索结果中没有年份
        """
        result = self._session.get('movie.search_douban', {
            'keyword': keyword
        })
        if not result:
            return []
        return [DoubanSearchResult(x) for x in result]

    def list_ranking(self, ranking_type: DoubanRankingType, proxy_pic: bool = False) -> Optional[
        List[DoubanRankingItem]]:
        """
        获取豆瓣榜单数据
        """
        res = self._session.get('douban.list_ranking', {
            'ranking_type': ranking_type.value,
            'proxy_pic': proxy_pic
        })
        if not res:
            return []
        return [DoubanRankingItem(x) for x in res.get('result')]

    def use_api_search(self, keyword: str, count: Optional[int] = None) -> List[ApiSearchItem]:
        """
        使用豆瓣移动端API进行搜索，此接口会含有年份信息
        """
        res = self._session.get('douban.use_api_search', {
            'keyword': keyword,
            'count': count
        })
        if not res or not res.get('items'):
            return []
        list_ = res.get('items')
        result = []
        for item in list_:
            result.append(ApiSearchItem(item))
        return result

    def daily_media(self) -> Optional[DoubanDailyMedia]:
        """
        获取豆瓣每日推荐
        """
        meta = self._session.get('common.daily_media')
        if not meta:
            return
        return DoubanDailyMedia(meta)
