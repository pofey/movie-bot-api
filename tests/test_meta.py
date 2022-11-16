from moviebotapi import MovieBotServer
from moviebotapi.core.models import MediaType
from moviebotapi.core.session import AccessKeySession
from tests.constant import SERVER_URL, ACCESS_KEY

server = MovieBotServer(AccessKeySession(SERVER_URL, ACCESS_KEY))


def test_get_cast_crew_by_douban():
    assert server.meta.get_cast_crew_by_douban(MediaType.Movie, 3804891)

def test_get_cast_crew_by_tmdb():
    assert server.meta.get_cast_crew_by_tmdb(MediaType.TV, 60059)