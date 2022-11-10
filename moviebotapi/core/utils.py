import datetime
import json
from typing import Dict, List, _GenericAlias

from moviebotapi.core.models import MediaType


def copy_value(source: Dict, target: object) -> None:
    if not source:
        return
    if not target or not target.__annotations__:
        return
    for name in target.__annotations__:
        anno = target.__annotations__[name]
        setattr(target, name, parse_value(anno, source.get(name)))


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
        return dict(value)


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
            return _dict_value
        elif func in [List, list]:
            return _list_value(value)
        elif func == MediaType:
            l = value.lower()
            if l == 'movie':
                return MediaType.Movie
            if l in ['tv', 'series']:
                return MediaType.TV
        elif isinstance(func, _GenericAlias):
            if func.__origin__ in [List, list]:
                list_ = _list_value(value)
                res = []
                for x in list_:
                    res.append(parse_value(func.__args__[0], x))
                return res
        return func(value)
    return value
