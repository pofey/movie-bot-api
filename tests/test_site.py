from moviebotapi import MovieBotServer
from moviebotapi.core.exceptions import ApiErrorException
from moviebotapi.core.session import AccessKeySession
from moviebotapi.site import SearchQuery, SearchType
from tests.constant import SERVER_URL, ACCESS_KEY

server = MovieBotServer(AccessKeySession(SERVER_URL, ACCESS_KEY))


def test_list():
    list_ = server.site.list()
    assert list_
    return list_


def test_set():
    list_ = test_list()
    list_[0].cookie = 'test'
    try:
        list_[0].save()
        assert False
    except ApiErrorException:
        assert True


def test_search_local():
    assert server.site.search_local(SearchQuery(SearchType.Keyword, '子弹列车'))


def test_list_local_torrents():
    assert server.site.list_local_torrents()
