from moviebotapi.core.session import Session
from moviebotapi.subscribe import SubscribeApi
from moviebotapi.user import UserApi


class MovieBotServer:
    def __init__(self, session: Session):
        self.user = UserApi(session)
        self.subscribe = SubscribeApi(session)
