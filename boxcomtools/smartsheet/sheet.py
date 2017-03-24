from boxcomtools.base.base_object import BaseObject


class Sheet(BaseObject):

    def __init__(self, o):
        self._base_object = o

        if isinstance(o, dict):
            for k, v in o.items():
                setattr(self, k, v)
    def to_dict():
        return self.__dict__
