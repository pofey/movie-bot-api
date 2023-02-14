import datetime
import decimal
import json
import os
import re
from enum import Enum
from typing import Dict, List, _GenericAlias, Optional

import cn2an

from moviebotapi.core.models import MediaType


def _parse_field_value(field_value):
    if isinstance(field_value, decimal.Decimal):  # Decimal -> float
        field_value = round(float(field_value), 2)
    elif isinstance(field_value, datetime.datetime):  # datetime -> str
        field_value = str(field_value)
    elif isinstance(field_value, list):
        field_value = [_parse_field_value(i) for i in field_value]
    if hasattr(field_value, 'to_json'):
        field_value = field_value.to_json()
    elif isinstance(field_value, Enum):
        field_value = field_value.name
    elif isinstance(field_value, Dict):
        val = {}
        for key_ in field_value:
            val[key_] = _parse_field_value(field_value[key_])
        field_value = val
    return field_value


def json_object(cls):
    def to_json(self):
        """
        Json序列化
        :param hidden_fields: 覆盖类属性 hidden_fields
        :return:
        """

        model_json = {}

        for column in self.__dict__:
            if hasattr(self, column):
                model_json[column] = _parse_field_value(getattr(self, column))
        if '_sa_instance_state' in model_json:
            del model_json['_sa_instance_state']
        return model_json

    cls.to_json = to_json

    return cls


def string_to_number(text):
    """
    文本转化成字符串，支持中文大写数字，如一百二十三
    :param text:
    :return:
    """
    if text is None:
        return None
    if text.isdigit():
        return int(text)
    else:
        try:
            return cn2an.cn2an(text)
        except ValueError as e:
            return None


def name_convert_to_camel(name: str) -> str:
    """下划线转驼峰(小驼峰)"""
    return re.sub(r'(_[a-z])', lambda x: x.group(1)[1].upper(), name)


def copy_value(source: Dict, target: object, camel_case=False) -> None:
    if not source:
        return
    if not target or not target.__annotations__:
        return
    for name in target.__annotations__:
        anno = target.__annotations__[name]
        setattr(target, name, parse_value(anno, source.get(name_convert_to_camel(name) if camel_case else name)))


def to_dict(obj: object) -> Optional[Dict]:
    if not obj or not obj.__annotations__:
        return
    result = {}
    for name in obj.__annotations__:
        anno = obj.__annotations__[name]
        result.update({name: parse_value(anno, getattr(obj, name))})
    return result


def _list_value(value):
    if isinstance(value, str):
        if value[0] in ['{', '[']:
            return json.loads(value)
        else:
            return value.split(',')
    else:
        return list(value)


def _dict_value(value):
    if isinstance(value, str):
        return json.loads(value)
    else:
        return value


def parse_value(func, value):
    if value is not None:
        if func == bool:
            if value in (1, True, "1", "true"):
                return True
            elif value in (0, False, "0", "false"):
                return False
            else:
                raise ValueError(value)

        elif func in (int, float):
            try:
                return func(value)
            except ValueError:
                return float('nan')
        elif func == datetime.datetime:
            return datetime.datetime.strptime(value, '%Y-%m-%d %H:%M:%S')
        elif func in [Dict, dict]:
            return _dict_value(value)
        elif func in [List, list]:
            return _list_value(value)
        elif func == MediaType:
            return MediaType.get(value)
        elif isinstance(func, _GenericAlias):
            if func.__origin__ in [List, list]:
                list_ = _list_value(value)
                res = []
                for x in list_:
                    res.append(parse_value(func.__args__[0], x))
                return res
        return func(value)
    return value


"""文件后缀"""
EXT_TYPE = {
    'info': ['.nfo', '.txt', '.cue'],
    'subtitle': ['.ass', '.srt', '.smi', '.ssa', '.sub', '.vtt', '.idx'],
    'image': ['.jpg', '.jpeg', '.png', '.gif', '.bmp', '.ico', '.tif'],
    'video': ['.mp4', '.mkv', '.avi', '.wmv', '.mpg', '.mpeg', '.mov', '.rm', '.rmvb', '.ram', '.flv', '.ts',
              '.iso', '.m2ts', '.bdmv'],
    'audio': ['.mka', '.mp3', '.m3u', '.flac']
}


def get_file_type(filepath):
    """
    获取一个文件的格式类型，基于后缀判断
    :param filepath:
    :return: info、subtitle、image、video、audio
    """
    if not EXT_TYPE:
        return 'unknown'
    ext = os.path.splitext(filepath)[-1].lower()
    for key in EXT_TYPE.keys():
        if ext in EXT_TYPE[key]:
            return key
    return 'unknown'


class _Countries:
    """ISO3166国家码处理工具"""
    iso3166_mapping: dict = dict()

    def __init__(self):
        with open(os.path.join(os.path.split(os.path.realpath(__file__))[0], 'country_mapping.txt'), 'r') as f:
            for line in f:
                line = line.strip('\n')
                if line == '':
                    continue
                arr = line.split('=')
                self.iso3166_mapping[arr[0]] = arr[1]

    def get(self, code):
        code = str(code).upper()
        if code in self.iso3166_mapping.keys():
            return self.iso3166_mapping[code]
        else:
            if '其他' in self.iso3166_mapping:
                return self.iso3166_mapping['其他']
            else:
                return '其他'


Countries = _Countries()
CN_EP_PATTERN = '[集话回話画期]'
TV_NUM_PATTERN = '[1234567890一二三四五六七八九十]{1,4}'
SEASON_NUM_PATTERN = '[1234567890一二三四五六七八九十]{1,3}'

SEASON_PATTERNS = [
    re.compile('[sS](%s)?[-—~]{1,3}[sS]?(%s)' % (SEASON_NUM_PATTERN, SEASON_NUM_PATTERN)),
    re.compile('第(%s)[季部辑]?分?[-—~]{1,3}第?(%s)[季部辑]分?' % (SEASON_NUM_PATTERN, SEASON_NUM_PATTERN)),
    re.compile(r'S(?:eason)?(\d{1,3})', re.IGNORECASE),
    re.compile(r'S(?:eason)?[-]{0,3}(\d{1,3})', re.IGNORECASE),
    re.compile('第(%s)[季部辑]分?' % SEASON_NUM_PATTERN),
    re.compile(r'S(?:eason)?\s(\d{1,3})', re.IGNORECASE)
]
COMPLETE_SEASON_PATTERNS = [
    re.compile('全(%s)[季部辑]' % SEASON_NUM_PATTERN)
]
EPISODE_PATTERNS = [
    re.compile(r'[Ee][Pp]?(%s)' % TV_NUM_PATTERN),
    re.compile('第?(%s)%s' % (TV_NUM_PATTERN, CN_EP_PATTERN)),
    re.compile(r'第\s?(%s)\s?%s' % (TV_NUM_PATTERN, CN_EP_PATTERN)),
    re.compile(r'^(%s)\s?$' % TV_NUM_PATTERN),
    re.compile(r'^(%s)\.' % TV_NUM_PATTERN),
    re.compile(r'(%s)[oO][fF]%s' % (TV_NUM_PATTERN, TV_NUM_PATTERN)),
    re.compile(r'[\[【](%s)[】\]]' % TV_NUM_PATTERN),
    re.compile(r'\s{1}-\s{1}(%s)' % TV_NUM_PATTERN)
]
EPISODE_RANGE_PATTERNS = [
    re.compile('第(%s)%s?-第?(%s)%s' % (TV_NUM_PATTERN, CN_EP_PATTERN, TV_NUM_PATTERN, CN_EP_PATTERN)),
    re.compile(r'[Ee][Pp]?(\d{1,4})[Ee][Pp]?(\d{1,4})'),
    re.compile(r'[Ee][Pp]?(\d{1,4})-[Ee]?[Pp]?(\d{1,4})'),
    re.compile(r'^(%s)[-到](%s)$' % (TV_NUM_PATTERN, TV_NUM_PATTERN)),
    re.compile(r'^(%s)\s{0,4}-\s{0,4}.+$' % TV_NUM_PATTERN),
    re.compile(r'[\[【\(](%s)-(%s)[】\]\)]' % (TV_NUM_PATTERN, TV_NUM_PATTERN)),
    re.compile(r'(全)(%s)%s' % (TV_NUM_PATTERN, CN_EP_PATTERN))
]
COMPLETE_EPISODE_PATTERNS = [
    re.compile('全(%s)%s' % (TV_NUM_PATTERN, CN_EP_PATTERN)),
    re.compile('(%s)%s全' % (TV_NUM_PATTERN, CN_EP_PATTERN)),
    re.compile('全%s' % CN_EP_PATTERN),
    re.compile('所有%s' % CN_EP_PATTERN)
]


class MediaParser:
    """媒体信息格式化工具类，待重构完成"""

    @staticmethod
    def parse_episode(text, match_single=True, match_range=True):
        if not text:
            return
        if get_file_type(text) != 'unknown':
            text = os.path.splitext(text)[0]
        ep_index_start = None
        ep_index_end = None
        ep_str = None
        pts = []
        if match_range:
            pts += EPISODE_RANGE_PATTERNS
        if match_single:
            pts += EPISODE_PATTERNS
        for p in pts:
            m = p.search(text)
            if m:
                ep_str = m.group()
                if len(m.groups()) == 1:
                    ep_index_start = string_to_number(m.group(1))
                    ep_index_end = None
                elif len(m.groups()) == 2:
                    ep_index_start = string_to_number(m.group(1))
                    ep_index_end = string_to_number(m.group(2))
                if ep_index_start and ep_index_start > 2000:
                    # is year,not episode
                    ep_index_start = None
                    ep_index_end = None
                    continue
                break
        if ep_index_start is None:
            return
        return {'start': ep_index_start, 'end': ep_index_end, 'text': ep_str}

    @staticmethod
    def parse_season(text):
        season_start = None
        season_end = None
        season_text = None
        for p in SEASON_PATTERNS:
            m = p.search(text)
            if m:
                season_text = m.group()
                if season_text == text:
                    season_text = m.group(1)
                if len(m.groups()) == 1:
                    season_start = string_to_number(m.group(1))
                    season_end = None
                elif len(m.groups()) == 2:
                    season_start = string_to_number(m.group(1))
                    season_end = string_to_number(m.group(2))
                break
        return {'start': season_start, 'end': season_end, 'text': season_text}

    @staticmethod
    def episode_format(episode, prefix=''):
        if not episode:
            return
        if isinstance(episode, str):
            episode = list(filter(None, episode.split(',')))
            episode = [int(i) for i in episode]
        elif isinstance(episode, int):
            episode = [episode]
        if episode:
            episode.sort()
        if len(episode) <= 2:
            return ','.join([str(e).zfill(2) for e in episode])
        else:
            episode.sort()
            return '%s%s-%s%s' % (prefix, str(episode[0]).zfill(2), prefix, str(episode[len(episode) - 1]).zfill(2))

    @staticmethod
    def trim_season(string):
        if not string:
            return
        string = str(string)
        season = MediaParser.parse_season(string)
        if season and season.get('text'):
            simple_name = string.replace(season.get('text'), '').strip()
        else:
            simple_name = string
        return simple_name
