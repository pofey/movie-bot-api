from moviebotapi import MovieBotServer
from moviebotapi.core.session import AccessKeySession
from tests.constant import SERVER_URL, ACCESS_KEY

server = MovieBotServer(AccessKeySession(SERVER_URL, ACCESS_KEY))


def test_get_default_ak():
    server.auth.get_default_ak()


def test_add_permission():
    server.auth.add_permission([1, 2], '/common/view#/static/tv_calendar.html')
