from typing import Dict, List, Optional

from moviebotapi import Session


class AuthApi:
    def __init__(self, session: Session):
        self._session: Session = session

    def get_default_ak(self, ) -> Dict:
        return self._session.get('auth.get_default_ak')

    def add_permission(self, role_code: List[int], uri: str):
        """
        为角色授权可访问的URI
        :param role_code: 角色码 1为管理员 2为普通用户，目前固定不变
        :param uri: 权限点URI
        :return:
        """
        self._session.post('auth.add_permission', {
            'role_code': role_code,
            'uri': uri
        })

    def get_cloud_access_token(self) -> Optional[str]:
        return self._session.get('auth.get_cloud_access_token')
