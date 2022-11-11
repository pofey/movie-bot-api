import datetime
from typing import Dict, List, Optional

from moviebotapi.core import utils
from moviebotapi.core.session import Session


class User:
    gmt_create: datetime.datetime
    gmt_modified: datetime.datetime
    username: str
    nickname: str
    douban_user: str
    qywx_user: str
    telegram_user_id: int
    bark_url: str
    avatar: str
    role: int
    pushdeer_key: str
    score_rule_name: str
    password: str

    def __init__(self, data: Dict, api: 'UserApi'):
        utils.copy_value(data, self)
        self._api = api
        self.uid: int = utils.parse_value(int, data.get('id'))

    def delete(self):
        self._api.delete(self.uid)

    def reset_password(self, new_password: str):
        self._api.reset_password(self.uid, new_password)

    def update(self):
        self._api.update(self)


class UserApi:
    def __init__(self, session: Session):
        self._session: Session = session

    def reset_password(self, uid: int, new_password: str):
        self._session.post('user.reset_password', json={'uid': uid, 'password': new_password})

    def delete(self, uid: int):
        self._session.post('user.delete_user', json={'uid': uid})

    def get(self, uid: int) -> Optional[User]:
        user = self._session.get('user.get_user', params={
            'id': uid
        })
        if not user:
            return
        return User(user, self)

    def update(self, user: User):
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

    def list(self) -> List[User]:
        list_ = self._session.get('user.get_user_list')
        if not list_:
            return []
        return [User(x, self) for x in list_]
