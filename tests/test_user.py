from moviebotapi import MovieBotServer
from moviebotapi.core.session import AccessKeySession
from tests.constant import ACCESS_KEY, SERVER_URL

server = MovieBotServer(AccessKeySession(SERVER_URL, ACCESS_KEY))


def test_get_user_list():
    assert server.user.list()


def test_get_user():
    user = server.user.get(1)
    assert user
    user.nickname = 'test'
    user.update()
    user = server.user.get(1)
    assert user
    assert user.nickname == 'test'


def test_upload_img_to_cloud_by_filepath():
    r = server.user.upload_img_to_cloud_by_filepath(
        '/Users/yee/workspace/test/movie-robot/plugins/annual_report/report.jpg')
    print(r)
