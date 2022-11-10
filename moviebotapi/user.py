import datetime
from typing import Dict, List, Optional

from moviebotapi.core import utils
from moviebotapi.core.session import Session


class User:
    def __init__(self, data: Dict, api: 'UserApi'):
        self._api = api
        self.gmt_create: datetime.datetime = utils.parse_value(datetime.datetime, data.get('gmt_create'))
        self.gmt_modified: datetime.datetime = utils.parse_value(datetime.datetime, data.get('gmt_modified'))
        self.uid: int = utils.parse_value(int, data.get('id'))
        self.username: str = utils.parse_value(str, data.get('username'))
        self.nickname: str = utils.parse_value(str, data.get('nickname'))
        self.douban_user: str = utils.parse_value(str, data.get('douban_user'))
        self.qywx_user: str = utils.parse_value(str, data.get('qywx_user'))
        self.telegram_user_id: int = utils.parse_value(int, data.get('telegram_user_id'))
        self.bark_url: str = utils.parse_value(str, data.get('bark_url'))
        self.avatar: str = utils.parse_value(str, data.get('avatar'))
        self.role: int = utils.parse_value(int, data.get('role'))
        self.user: str = utils.parse_value(str, data.get('qywx_user'))
        self.pushdeer_key: str = utils.parse_value(str, data.get('pushdeer_key'))
        self.score_rule_name: str = utils.parse_value(str, data.get('score_rule_name'))
        self.password: str = utils.parse_value(str, data.get('password'))

    def delete_user(self):
        self._api.delete_user(self.uid)

    def reset_password(self, new_password: str):
        self._api.reset_password(self.uid, new_password)

    def update_user(self):
        self._api.update_user(self)


class UserApi:
    def __init__(self, session: Session):
        self._session: Session = session

    def reset_password(self, uid: int, new_password: str):
        self._session.post('user.reset_password', json={'uid': uid, 'password': new_password})

    def delete_user(self, uid: int):
        self._session.post('user.delete_user', json={'uid': uid})

    def get_user(self, uid: int) -> Optional[User]:
        user = self._session.get('user.get_user', params={
            'id': uid
        })
        if not user:
            return
        return User(user, self)

    def update_user(self, user: User):
        self._session.post('user.update_user', json={
            'uid': user.uid,
            'username': user.username,
            'nickname': user.nickname,
            'new_password': user.password,
            'role': user.role,
            'douban_user': user.douban_user,
            'qywx_user': user.qywx_user,
            'pushdeer_key': user.pushdeer_key,
            'bark_url': user.bark_url,
            'score_rule_name': user.score_rule_name,
            'telegram_user_id': user.telegram_user_id
        })

    def get_user_list(self) -> List[User]:
        list_ = self._session.get('user.get_user_list')
        if not list_:
            return []
        return [User(x, self) for x in list_]
