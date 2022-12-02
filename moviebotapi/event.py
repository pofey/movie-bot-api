from typing import Dict

from moviebotapi import Session


class EventApi:
    def __init__(self, session: Session):
        self._session: Session = session

    def publish_event(self, event_name: str, event_data: Dict):
        """
        发布事件，订阅者可以订阅
        事件名称建议采用每个单词首字母大写的方式来命名
        """
        self._session.post('event.publish_event', {
            'event_name': event_name,
            'event_data': event_data
        })
