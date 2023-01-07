import base64

import httpx

from moviebotapi import MovieBotServer
from moviebotapi.core.session import AccessKeySession
from tests.constant import SERVER_URL, ACCESS_KEY

server = MovieBotServer(AccessKeySession(SERVER_URL, ACCESS_KEY))


def test_cache():
    server.common.set_cache('test', 'a', {'aaa': 123})
    assert server.common.get_cache('test', 'a').get('aaa') == 123


def test_get_image_text():
    with open('image.png', "rb") as f:
        base64_data = base64.b64encode(f.read())
    print(server.common.get_image_text(base64_data.decode()))

def test_get_cache_image_filepath():
    print(server.common.get_cache_image_filepath('https://image.tmdb.org/t/p/original/xEggmiD4WoJBQR2AiVF46yPUUgD.jpg'))