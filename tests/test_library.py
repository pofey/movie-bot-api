from moviebotapi import MovieBotServer
from moviebotapi.core.models import MediaType
from moviebotapi.core.session import AccessKeySession
from moviebotapi.library import MediaLibraryPath, TransferMode
from tests.constant import SERVER_URL, ACCESS_KEY

server = MovieBotServer(AccessKeySession(SERVER_URL, ACCESS_KEY))


def test_start_scanner():
    server.library.start_scanner(1)


def test_stop_scanner():
    server.library.stop_scanner(1)


def test_add_library():
    path = MediaLibraryPath()
    path.path = '/Volumes/media/plex/电影/港台'
    server.library.add_library(MediaType.Movie, '港台电影', [path])


def test_rename_by_path():
    server.library.rename_by_path('/Volumes/media/plex/电影/港台')


def test_direct_transfer():
    server.library.direct_transfer('/media/电影/港台', '/media/plex/电影/港台', TransferMode.HardLink)
