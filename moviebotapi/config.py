from typing import Dict

import yaml

from moviebotapi import Session
from moviebotapi.core import utils
from moviebotapi.core.utils import json_object


@json_object
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


@json_object
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


@json_object
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


@json_object
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

    def register_channel_template(self, tmpl_filepath: str):
        """
        注册一个通道模版文件
        模版示范可以参考conf/notify_template 目录内自带模版文件，此模版内包含了所有系统通知的内容格式
        :param tmpl_filepath: 模版文件路径
        :return:
        """
        with open(tmpl_filepath, 'r', encoding='utf-8') as file:
            tmpl = yaml.safe_load(file)
        self._session.post('setting.register_channel_template', tmpl)
