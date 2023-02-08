import os
import urllib

import httpx
from httpx import Timeout

REPO = 'http://127.0.0.1:8080'
USER_AGENT = 'movie-bot-plugin/0.1'


def reset_password(license_key):
    """
    通过Licese重置登陆密码
    :param license_key:
    :return:
    """
    r = httpx.get(
        url=f'{REPO}/api/user/resetPasswordByLicense?licenseKey={license_key}',
        headers={'User-Agent': USER_AGENT}
    )
    j = r.json()
    print(j.get('message'))


def get_ak(email, password):
    r = httpx.post(
        url=f'{REPO}/api/auth/createAccessTokenByEmail',
        json={
            'email': email,
            'password': password
        },
        headers={'User-Agent': USER_AGENT},
        timeout=Timeout(30)
    )
    j = r.json()
    if j.get('data'):
        return j.get('data').get('accessToken')
    else:
        print(j.get('message'))
    return None


def publish(ak, plugin_zip_path, change_log):
    if not os.path.exists(plugin_zip_path):
        print(f'插件压缩包路径不存在：{plugin_zip_path}')
        return
    if os.path.splitext(plugin_zip_path)[-1].lower() != '.zip':
        print(f'仅支持zip格式插件包发布')
        return
    files = {'file': (os.path.split(plugin_zip_path)[-1], open(plugin_zip_path, 'rb'), 'application/zip')}
    r = httpx.post(
        f'{REPO}/api/plugins/publish?changeLog={urllib.parse.quote_plus(change_log)}',
        files=files,
        headers={
            'token': ak,
            'User-Agent': USER_AGENT
        },
        timeout=Timeout(30)
    )
    print(r.text)


if __name__ == '__main__':
    ak = get_ak('xx', 'xx')
    publish(
        ak,
        '/Users/yee/Library/Containers/com.tencent.xinWeChat/Data/Library/Application Support/com.tencent.xinWeChat/2.0b4.0.9/f4ba1fd4852be9ffffae3a6d5d7065f3/Message/MessageTemp/4dce4cee3ce4cfdc18a754c065cb9014/File/site_signin.zip',
        '''修复部分站点签到失败的bug
        开放定时签到时间设置'''
    )
