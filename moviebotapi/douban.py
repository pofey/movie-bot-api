from enum import Enum
from typing import Dict, List, Optional

from moviebotapi import Session
from moviebotapi.core import utils
from moviebotapi.core.models import MediaType
from moviebotapi.subscribe import SubStatus


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


class DoubanApi:
    def __init__(self, session: Session):
        self._session: Session = session

    def get(self, douban_id: int) -> Optional[DoubanMedia]:
        meta = self._session.get('douban.get', {
            'douban_id': douban_id
        })
        if not meta:
            return
        return DoubanMedia(meta)

    def search(self, keyword: str) -> List[DoubanSearchResult]:
        result = self._session.get('movie.search_douban', {
            'keyword': keyword
        })
        if not result:
            return []
        return [DoubanSearchResult(x) for x in result]

    def list_ranking(self, ranking_type: DoubanRankingType, proxy_pic: bool = False) -> Optional[
        List[DoubanRankingItem]]:
        res = self._session.get('douban.list_ranking', {
            'ranking_type': ranking_type.value,
            'proxy_pic': proxy_pic
        })
        if not res:
            return []
        return [DoubanRankingItem(x) for x in res.get('result')]
