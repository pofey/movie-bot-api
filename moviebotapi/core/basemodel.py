from moviebotapi.core import utils


class BaseModel(object):

    def to_json(self, hidden_fields=None):
        """
        Json序列化
        :param hidden_fields: 覆盖类属性 hidden_fields
        :return:
        """
        model_json = {}
        if not hidden_fields:
            hidden_fields = []
        for column in self.__dict__:
            if column in hidden_fields:
                continue
            if hasattr(self, column):
                model_json[column] = utils.parse_field_value(getattr(self, column))
        if '_sa_instance_state' in model_json:
            del model_json['_sa_instance_state']
        return model_json
