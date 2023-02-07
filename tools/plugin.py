import os

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


def publish(ak, plugin_zip_path):
    if not os.path.exists(plugin_zip_path):
        print(f'插件压缩包路径不存在：{plugin_zip_path}')
        return
    if os.path.splitext(plugin_zip_path)[-1].lower() != '.zip':
        print(f'仅支持zip格式插件包发布')
        return
    files = {'file': (os.path.split(plugin_zip_path)[-1], open(plugin_zip_path, 'rb'), 'application/zip')}
    r = httpx.post(
        f'{REPO}/api/plugins/publish',
        files=files,
        headers={
            'token': ak,
            'User-Agent': USER_AGENT
        },
        timeout=Timeout(30)
    )
    print(r.text)


if __name__ == '__main__':
    ak = get_ak('xxx', 'xxx')
    publish(ak, '/xxx.zip')
