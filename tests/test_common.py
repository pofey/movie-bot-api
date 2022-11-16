from moviebotapi import MovieBotServer
from moviebotapi.core.session import AccessKeySession
from tests.constant import SERVER_URL, ACCESS_KEY

server = MovieBotServer(AccessKeySession(SERVER_URL, ACCESS_KEY))


def test_cache():
    server.common.set_cache('test', 'a', {'aaa': 123})
    assert server.common.get_cache('test', 'a').get('aaa') == 123