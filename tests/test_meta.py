from moviebotapi import MovieBotServer
from moviebotapi.core.models import MediaType
from moviebotapi.core.session import AccessKeySession
from tests.constant import SERVER_URL, ACCESS_KEY

server = MovieBotServer(AccessKeySession(SERVER_URL, ACCESS_KEY))


def test_get_cast_crew_by_douban():
    assert server.meta.get_cast_crew_by_douban(MediaType.Movie, 3804891)


def test_get_cast_crew_by_tmdb():
    assert server.meta.get_cast_crew_by_tmdb(MediaType.TV, 60059)


def test_get_media_by_tmdb_id():
    assert server.meta.get_media_by_tmdb(MediaType.TV, 60059)


def test_get_media_by_douban_id():
    assert server.meta.get_media_by_douban(MediaType.Movie, 1889243)


def test_share_meta_from_id():
    print(server.meta.share_meta_from_id(872176, 35415401))
