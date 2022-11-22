from moviebotapi import MovieBotServer
from moviebotapi.core.session import AccessKeySession
from tests.constant import SERVER_URL, ACCESS_KEY

server = MovieBotServer(AccessKeySession(SERVER_URL, ACCESS_KEY))


def test_send_text_message():
    server.notify.send_system_message(1, 'test', 'aaaa')


def test_send_message_by_tmpl():
    server.notify.send_message_by_tmpl('{{title}}', '{{a}}', {
        'title': '我是标题',
        'a': "hello",
        'link_url': 'http://www.bing.com',
        'pic_url': 'https://www.curvearro.com/wp-content/uploads/sites/1/2020/10/Microsoft-Bing-Banner-1.jpg'
    })
