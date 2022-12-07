from moviebotapi import MovieBotServer
from moviebotapi.core.session import AccessKeySession
from tests.constant import SERVER_URL, ACCESS_KEY

server = MovieBotServer(AccessKeySession(SERVER_URL, ACCESS_KEY))


def test_parse_name_meta_by_string():
    print(server.amr.parse_name_meta_by_string(
        '人世间.CCTV1.A.Lifelong.Journey.S01E01.2022.1080i.HDTV.H264.AC3-iLoveTV').__dict__)


def test_parse_name_meta_by_filepath():
    print(server.amr.parse_name_meta_by_filepath(
        '/Users/yee/workspace/test_media/download/this.is.us/Season 6/this.is.us.s06e05.720p.hdtv.x264-syncopy.mkv').__dict__)


def test_analysis_string():
    print(server.amr.analysis_string('人世间.CCTV1.A.Lifelong.Journey.S01E01.2022.1080i.HDTV.H264.AC3-iLoveTV').__dict__)


def test_analysis_douban_meta():
    print(server.amr.analysis_douban_meta('人世间', year=2022).__dict__)
