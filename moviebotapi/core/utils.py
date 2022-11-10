import datetime
import json
from typing import Dict

from moviebotapi.core.models import MediaType


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
        elif func == Dict:
            if isinstance(value, str):
                return json.loads(value)
            else:
                return value
        elif func == MediaType:
            return MediaType(value)
        return func(value)
    return value
