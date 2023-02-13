from typing import Dict, List

from moviebotapi import Session
from moviebotapi.core import utils


class PluginMeta:
    id: int
    plugin_name: str
    title: str
    author: str
    config_field: list
    dependencies: dict
    description: str
    github_url: str
    help_doc_url: str
    local_version: str
    logo_url: str
    version: str
    plugin_folder: str

    def __init__(self, data: Dict):
        utils.copy_value(data, self, True)


class PluginApi:
    def __init__(self, session: Session):
        self._session: Session = session

    def get_installed_list(self) -> List[PluginMeta]:
        """
        获取本地安装的插件列表
        """
        r = self._session.get('plugins.get_installed_list')
        if not r:
            return []
        res = []
        for item in r:
            res.append(PluginMeta(item))
        return res
