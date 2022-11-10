from moviebotapi import MovieBotServer
from moviebotapi.core.session import AccessKeySession
from tests.constant import ACCESS_KEY, SERVER_URL

server = MovieBotServer(AccessKeySession(SERVER_URL, ACCESS_KEY))


def test_get_user_list():
    assert server.user.list()


def test_get_user():
    user = server.user.get(1)
    assert user
    user.nickname = 'test'
    user.update()
    user = server.user.get(1)
    assert user
    assert user.nickname == 'test'
