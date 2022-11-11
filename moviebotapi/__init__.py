from moviebotapi.core.session import Session
from moviebotapi.douban import DoubanApi
from moviebotapi.notify import NotifyApi
from moviebotapi.scraper import ScraperApi
from moviebotapi.site import SiteApi
from moviebotapi.subscribe import SubscribeApi
from moviebotapi.tmdb import TmdbApi
from moviebotapi.user import UserApi


class MovieBotServer:
    user: UserApi
    subscribe: SubscribeApi
    scraper: ScraperApi
    douban: DoubanApi
    tmdb: TmdbApi
    site: SiteApi
    notify: NotifyApi

    def __init__(self, session: Session = None):
        if session:
            self.set_session(session)

    def set_session(self, session: Session):
        self.user = UserApi(session)
        self.subscribe = SubscribeApi(session)
        self.scraper = ScraperApi(session)
        self.douban = DoubanApi(session)
        self.tmdb = TmdbApi(session)
        self.site = SiteApi(session)
        self.notify = NotifyApi(session)
