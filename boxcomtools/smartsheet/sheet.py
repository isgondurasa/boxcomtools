from boxcomtools.base.base_object import BaseObject


class Sheet(BaseObject):

    def __init__(self, session, object_id, **kwargs):
        super(Sheet, self).__init__(session, object_id)
        
        for k, v in kwargs.items():
            if k != 'id':
                setattr(self, k, v)

    def to_dict():
        return self.__dict__
