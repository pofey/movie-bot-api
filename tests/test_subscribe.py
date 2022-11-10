from moviebotapi import MovieBotServer
from moviebotapi.core.session import AccessKeySession
from moviebotapi.subscribe import SubStatus
from tests.constant import SERVER_URL, ACCESS_KEY

server = MovieBotServer(AccessKeySession(SERVER_URL, ACCESS_KEY))


def test_list():
    server.subscribe.list(status=SubStatus.Subscribing)
