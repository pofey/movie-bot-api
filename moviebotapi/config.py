from typing import Dict

from moviebotapi import Session
from moviebotapi.core import utils


class DoubanConfig:
    cookie: str

    def __init__(self, data: Dict, session: Session):
        utils.copy_value(data, self)
        self._ = session

    def save(self):
        """
        保存豆瓣配置，保存过程服务端会检查cookie的有效性，不是简单的保存配置文件
        """
        self._.post('setting.save_douban', json={
            'cookie': self.cookie
        })


class FreeDownloadConfig:
    available_space: int
    avg_statistics_period: int
    enable: bool
    maximum_active_torrent: int
    save_path: str
    upload_mbps_maximum: int

    def __init__(self, data: Dict, session: Session):
        utils.copy_value(data, self)
        self._ = session

    def save(self):
        self._.post('setting.save_free_download', json={
            'enable': self.enable,
            'save_path': self.save_path,
            'available_space': self.available_space,
            'avg_statistics_period': self.avg_statistics_period,
            'upload_mbps_maximum': self.upload_mbps_maximum,
            'maximum_active_torrent': self.maximum_active_torrent
        })


class ConfigApi:
    def __init__(self, session: Session):
        self._session: Session = session

    @property
    def douban(self):
        return DoubanConfig(self._session.get('setting.get_douban'), self._session)

    @property
    def free_download(self):
        return FreeDownloadConfig(self._session.get('setting.get_free_download'), self._session)
