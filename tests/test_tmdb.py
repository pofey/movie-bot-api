from moviebotapi import MovieBotServer
from moviebotapi.core.models import MediaType
from moviebotapi.core.session import AccessKeySession
from moviebotapi.ext import MediaMetaSelect
from tests.constant import SERVER_URL, ACCESS_KEY

server = MovieBotServer(AccessKeySession(SERVER_URL, ACCESS_KEY))


def test_get():
    meta = MediaMetaSelect(tmdb=server.tmdb.get(MediaType.Movie, 436270))
    assert meta


def test_search():
    server.tmdb.search(MediaType.Movie, '子弹列车')


def test_search_multi():
    server.tmdb.search_multi('权利的堡垒')


def test_get_aka_names():
    server.tmdb.get_aka_names(MediaType.Movie, 985939)
