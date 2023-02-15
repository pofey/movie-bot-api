
from moviebotapi.core import utils


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
                model_json[column] = utils.parse_field_value(getattr(self, column))
        if '_sa_instance_state' in model_json:
            del model_json['_sa_instance_state']
        return model_json
