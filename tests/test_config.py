from moviebotapi import MovieBotServer
from moviebotapi.core.models import MediaType
from moviebotapi.core.session import AccessKeySession
from tests.constant import SERVER_URL, ACCESS_KEY

server = MovieBotServer(AccessKeySession(SERVER_URL, ACCESS_KEY))


def test_get_and_set():
    free_download = server.config.free_download
    free_download.enable = False
    free_download.save()


def test_get_web_config():
    print(server.config.web.server_url)


def test_get_env():
    print(server.config.env.user_config_dir)
