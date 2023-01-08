import base64

import httpx

from moviebotapi import MovieBotServer
from moviebotapi.common import MenuItem
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


def test_list_menus():
    menus = server.common.list_menus()
    for item in menus:
        if item.title == '我的':
            test = MenuItem()
            test.title = '追剧日历'
            test.href = '/common/view#/static/tv_calendar.html'
            test.icon = 'AcUnit'
            item.pages.append(test)
            break
    server.common.save_menus(menus)
