def ignore_attr_not_exists(cls):
    """
    忽略属性不存在的异常，正常返回空结果
    """
    orig_getattribute = cls.__getattribute__

    def getattribute(self, attr):
        if not hasattr(cls, attr):
            return
        return orig_getattribute(self, attr)

    cls.__getattribute__ = getattribute
    return cls
