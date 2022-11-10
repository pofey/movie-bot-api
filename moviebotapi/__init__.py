from moviebotapi.core.session import Session
from moviebotapi.douban import DoubanApi
from moviebotapi.scraper import ScraperApi
from moviebotapi.site import SiteApi
from moviebotapi.subscribe import SubscribeApi
from moviebotapi.tmdb import TmdbApi
from moviebotapi.user import UserApi


class MovieBotServer:
    def __init__(self, session: Session):
        self.user = UserApi(session)
        self.subscribe = SubscribeApi(session)
        self.scraper = ScraperApi(session)
        self.douban = DoubanApi(session)
        self.tmdb = TmdbApi(session)
        self.site = SiteApi(session)
