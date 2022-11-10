import datetime
from enum import Enum
from typing import Dict

from moviebotapi import Session
from moviebotapi.core import utils


class TrafficManagementStatus(int, Enum):
    Disabled = 0
    Initiative = 1
    Passive = 2


class SiteStatus(int, Enum):
    Normal = 1
    Error = 2


class Site:
    gmt_modified: datetime.datetime
    uid: int
    username: str
    cookie: str
    web_search: bool
    smart_download: bool
    share_rate: float
    upload_size: float
    download_size: float
    is_vip: bool
    status: SiteStatus
    traffic_management_status: TrafficManagementStatus
    # 主动模式时上传流量目标，单位GB
    upload_kpi: int
    proxies: str
    user_agent: str

    def __init__(self, data: Dict, api: "SiteApi"):
        utils.copy_value(data, self)
        self.site_id: str = utils.parse_value(str, data.get('site_name'))
        self.site_name: str = utils.parse_value(str, data.get('alias'))
        self._api = api


class SiteApi:
    def __init__(self, session: Session):
        self._session: Session = session

    def list(self):
        list_ = self._session.get('site.get_sites')
        if not list_:
            return
        return [Site(x, self) for x in list_]
