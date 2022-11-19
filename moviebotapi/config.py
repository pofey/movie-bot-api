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


class ConfigApi:
    def __init__(self, session: Session):
        self._session: Session = session

    @property
    def douban(self):
        return DoubanConfig(self._session.get('setting.get_douban'), self._session)
