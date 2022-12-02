from abc import ABCMeta, abstractmethod
from typing import Union, Dict, Sequence, Tuple, Optional, Any

import httpx
from httpx import Timeout

from moviebotapi.core.exceptions import ApiErrorException, NetworkErrorException, IllegalAuthorization

UA = 'moviebotapi/0.0.34'
URLTypes = Union["URL", str]
HeaderTypes = Union[
    "Headers",
    Dict[str, str],
    Dict[bytes, bytes],
    Sequence[Tuple[str, str]],
    Sequence[Tuple[bytes, bytes]],
]


class Session(metaclass=ABCMeta):
    @staticmethod
    def un_code(res):
        if res:
            if res.get('code') == 0:
                return res.get('data')
            if res.get('code') == 1:
                raise ApiErrorException(res.get('message'))
        else:
            return

    @abstractmethod
    def post(self, api_code: str, json: Optional[Any] = None, headers: Optional[HeaderTypes] = None):
        pass

    @abstractmethod
    def get(self, api_code: str, params: Optional[Dict[str, Any]] = None, headers: Optional[HeaderTypes] = None):
        pass


class AccessKeySession(Session):
    def __init__(self, server_url: URLTypes, access_key: str):
        self.server_url: URLTypes = server_url
        self.access_key: str = access_key
        self.timeout = Timeout(30)

    def _get_headers(self, headers: Optional[HeaderTypes] = None):
        if not headers:
            headers = {}
        headers.update({'AccessKey': self.access_key})
        headers.update({'User-Agent': UA})
        return headers

    @staticmethod
    def _get_api_uri(api_code: str):
        if not api_code:
            return
        return '/api/' + api_code.replace('.', '/')

    def get(self, api_code: str, params: Optional[Dict[str, Any]] = None, headers: Optional[HeaderTypes] = None):
        r = httpx.get(f'{self.server_url}{self._get_api_uri(api_code)}', params=params,
                      headers=self._get_headers(headers),
                      timeout=self.timeout)
        if not r:
            raise NetworkErrorException()
        if r.status_code == 401:
            raise IllegalAuthorization()
        r.raise_for_status()
        return self.un_code(r.json())

    def post(self, api_code: str, json: Optional[Any] = None, headers: Optional[HeaderTypes] = None):
        r = httpx.post(f'{self.server_url}{self._get_api_uri(api_code)}', json=json, headers=self._get_headers(headers),
                       timeout=self.timeout)
        if not r:
            raise NetworkErrorException()
        r.raise_for_status()
        return self.un_code(r.json())
