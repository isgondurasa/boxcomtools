from boxcomtools.base.base_object import BaseObject
from boxcomtools.base.config import SmartsheetConfig

class Sheet(BaseObject, SmartsheetConfig):

    __resource__ = "sheets"
    
    def __init__(self, session, object_id, **kwargs):
        super(Sheet, self).__init__(session, object_id)

        print("obj id")
        print(self._object_id)
        
        for k, v in kwargs.items():
            if k != 'id':
                setattr(self, k, v)
                
    def to_dict():
        return self._data
