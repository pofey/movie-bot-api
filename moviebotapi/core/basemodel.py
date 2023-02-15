import datetime
import decimal
from enum import Enum
from typing import Dict


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


class BaseModel(object):

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
