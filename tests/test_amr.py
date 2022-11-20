from moviebotapi import MovieBotServer
from moviebotapi.core.session import AccessKeySession
from tests.constant import SERVER_URL, ACCESS_KEY

server = MovieBotServer(AccessKeySession(SERVER_URL, ACCESS_KEY))


def test_parse_name_meta_by_string():
    print(server.amr.parse_name_meta_by_string(
        '人世间.CCTV1.A.Lifelong.Journey.S01E01.2022.1080i.HDTV.H264.AC3-iLoveTV').__dict__)


def test_parse_name_meta_by_filepath():
    print(server.amr.parse_name_meta_by_filepath(
        '/media_source/蜘蛛侠：英雄归来.Spider-Man.Homecoming.2017.BluRay.2160p.x265.10bit.HDR.3Audio.mUHD-FRDS').__dict__)
