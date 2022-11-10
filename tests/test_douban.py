from moviebotapi import MovieBotServer
from moviebotapi.core.models import MediaType
from moviebotapi.core.session import AccessKeySession
from tests.constant import SERVER_URL, ACCESS_KEY

server = MovieBotServer(AccessKeySession(SERVER_URL, ACCESS_KEY))


def test_get():
    meta = server.douban.get(35196753)
    assert meta
    assert meta.media_type == MediaType.TV


def test_search():
    assert server.douban.search('子弹列车')
