from moviebotapi import MovieBotServer
from moviebotapi.core.session import AccessKeySession
from tests.constant import SERVER_URL, ACCESS_KEY

server = MovieBotServer(AccessKeySession(SERVER_URL, ACCESS_KEY))


def test_get_episodes_from_tmdb():
    server.media_server.list_episodes_from_tmdb(94997, 1)


def test_search_by_tmdb():
    server.media_server.search_by_tmdb(94997)
