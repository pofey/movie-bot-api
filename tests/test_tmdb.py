from moviebotapi import MovieBotServer
from moviebotapi.core.models import MediaType
from moviebotapi.core.session import AccessKeySession
from moviebotapi.ext import MediaMetaSelect
from tests.constant import SERVER_URL, ACCESS_KEY

server = MovieBotServer(AccessKeySession(SERVER_URL, ACCESS_KEY))


def test_get():
    meta = MediaMetaSelect(tmdb=server.tmdb.get(MediaType.Movie, 496243))
    assert meta

