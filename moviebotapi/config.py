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


class WebConfig:
    """web访问配置"""
    host: str
    port: int
    # 外网访问地址
    server_url: str

    def __init__(self, data: Dict, session: Session):
        utils.copy_value(data, self)
        self._ = session

    def save(self):
        self._.post('setting.save_web', json={
            'host': self.host,
            'port': self.port,
            'server_url': self.server_url
        })


class Env:
    config_dir: str
    user_config_dir: str
    site_config_dir: str
    plugin_dir: str

    def __init__(self, data: Dict):
        utils.copy_value(data, self)


class ConfigApi:
    def __init__(self, session: Session):
        self._session: Session = session

    @property
    def douban(self):
        return DoubanConfig(self._session.get('setting.get_douban'), self._session)

    @property
    def free_download(self):
        return FreeDownloadConfig(self._session.get('setting.get_free_download'), self._session)

    @property
    def web(self):
        return WebConfig(self._session.get('setting.get_web'), self._session)

    @property
    def env(self):
        return Env(self._session.get('setting.get_env'))
