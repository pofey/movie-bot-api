from moviebotapi import MovieBotServer
from moviebotapi.core.models import MediaType
from moviebotapi.core.session import AccessKeySession
from moviebotapi.library import MediaLibraryPath, TransferMode
from tests.constant import SERVER_URL, ACCESS_KEY

server = MovieBotServer(AccessKeySession(SERVER_URL, ACCESS_KEY))


def test_start_scanner():
    """
    按编号扫描一个媒体库，此过程会分析媒体库内所有视频文件的影片数据、视频流信息
    此过程不破坏物理文件
    """
    server.library.start_scanner(1)


def test_stop_scanner():
    server.library.stop_scanner(1)


def test_add_library():
    """
    创建一个媒体库，并设置一个媒体库的路径
    """
    path = MediaLibraryPath()
    path.path = '/Volumes/media/plex/电影'
    server.library.add_library(MediaType.Movie, '电影', [path])


def test_rename_by_path():
    """
    对一个路径做文件名重建，重命名的模版采用识别与整理设置中的模版
    做此测试，可以选择硬连接一个单独的目录，会实际改变物理文件
    """
    server.library.rename_by_path('/Volumes/media/plex/电影')


def test_direct_transfer():
    server.library.direct_transfer('/media/电影/港台', '/media/plex/电影/港台', TransferMode.HardLink)
