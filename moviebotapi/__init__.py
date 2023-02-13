from moviebotapi.core.session import Session
from moviebotapi.douban import DoubanApi
from moviebotapi.event import EventApi
from moviebotapi.library import LibraryApi
from moviebotapi.mediaserver import MediaServerApi
from moviebotapi.meta import MetaApi
from moviebotapi.notify import NotifyApi
from moviebotapi.plugin import PluginApi
from moviebotapi.scraper import ScraperApi
from moviebotapi.site import SiteApi
from moviebotapi.subscribe import SubscribeApi
from moviebotapi.tmdb import TmdbApi
from moviebotapi.user import UserApi
from moviebotapi.config import ConfigApi
from moviebotapi.common import CommonApi
from moviebotapi.amr import AmrApi
from moviebotapi.auth import AuthApi


class MovieBotServer:
    session: Session
    user: UserApi
    subscribe: SubscribeApi
    scraper: ScraperApi
    douban: DoubanApi
    tmdb: TmdbApi
    site: SiteApi
    notify: NotifyApi
    config: ConfigApi
    meta: MetaApi
    common: CommonApi
    amr: AmrApi
    library: LibraryApi
    auth: AuthApi
    event: EventApi
    media_server: MediaServerApi
    plugin: PluginApi

    def __init__(self, session: Session = None):
        if session:
            self.set_session(session)

    def set_session(self, session: Session):
        self.session = session
        self.config = ConfigApi(session)
        self.user = UserApi(session)
        self.subscribe = SubscribeApi(session)
        self.scraper = ScraperApi(session)
        self.douban = DoubanApi(session)
        self.tmdb = TmdbApi(session)
        self.site = SiteApi(session)
        self.notify = NotifyApi(session)
        self.meta = MetaApi(session)
        self.common = CommonApi(session)
        self.amr = AmrApi(session)
        self.library = LibraryApi(session)
        self.auth = AuthApi(session)
        self.event = EventApi(session)
        self.media_server = MediaServerApi(session)
        self.plugin = PluginApi(session)
