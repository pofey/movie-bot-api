import os
import urllib

import click
import httpx
from httpx import Timeout

REPO = 'http://api.xmoviebot.com'
USER_AGENT = 'movie-bot-plugin/0.1'


@click.command()
@click.option('--license_key', prompt='请提供你的LicenseKey进行密码重置')
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


@click.command()
@click.option('--email', prompt='MovieBot邮件地址')
@click.option('--password', prompt='密码', hide_input=True)
@click.option('--plugin_zip_path', prompt='请输入插件压缩包（zip）完整路径')
@click.option('--change_log', prompt='请输入变更日志')
def publish(email, password, plugin_zip_path, change_log):
    if not os.path.exists(plugin_zip_path):
        print(f'插件压缩包路径不存在：{plugin_zip_path}')
        return
    if os.path.splitext(plugin_zip_path)[-1].lower() != '.zip':
        print(f'仅支持zip格式插件包发布')
        return
    ak = get_ak(email, password)
    if not ak:
        print('登录失败')
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
    j = r.json()
    print(j.get('message'))


@click.command()
@click.option('--action', '-a', prompt='选择需要进行的操作 reset 或 publish 分别为重制密码、发布或更新插件',
              type=click.Choice(['reset', 'publish']),
              help='选择需要进行的操作 reset 或 publish 分别为重制密码、发布或更新插件')
def select_action(action):
    if action == 'reset':
        reset_password()
    elif action == 'publish':
        print('需要登录MovieBot官方仓库后进行发布')
        publish()


if __name__ == '__main__':
    print(f'插件中心服务器：{REPO}')
    select_action()
