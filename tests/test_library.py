from moviebotapi import MovieBotServer
from moviebotapi.core.models import MediaType
from moviebotapi.core.session import AccessKeySession
from moviebotapi.library import MediaLibraryPath
from tests.constant import SERVER_URL, ACCESS_KEY

server = MovieBotServer(AccessKeySession(SERVER_URL, ACCESS_KEY))


def test_start_scanner():
    server.library.start_scanner(1)


def test_stop_scanner():
    server.library.stop_scanner(1)


def test_add_library():
    path = MediaLibraryPath()
    path.path = '/Volumes/media/电影/欧美'
    server.library.add_library(MediaType.Movie, '欧美电影', [path])
