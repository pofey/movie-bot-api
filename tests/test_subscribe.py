from moviebotapi import MovieBotServer
from moviebotapi.core.session import AccessKeySession
from moviebotapi.subscribe import SubStatus
from tests.constant import SERVER_URL, ACCESS_KEY

server = MovieBotServer(AccessKeySession(SERVER_URL, ACCESS_KEY))


def test_list():
    list_ = server.subscribe.list(status=SubStatus.Subscribing)
    assert list_
    return list_


def test_get():
    list_ = test_list()
    assert server.subscribe.get(list_[0].id)


def test_sub():
    server.subscribe.sub_by_douban(26654184)
