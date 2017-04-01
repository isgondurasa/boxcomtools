import logging
from boxcomtools.base.base_object import BaseObject
from boxcomtools.base.config import SmartsheetConfig


class Sheet(BaseObject, SmartsheetConfig):

    __resource__ = "sheets"
    
    def __init__(self, session, object_id=None, **kwargs):
        super(Sheet, self).__init__(session, object_id)
        
        for k, v in kwargs.items():
            if k != 'id':
                setattr(self, k, v)

    async def create(self, data):
        """
        curl https://api.smartsheet.com/2.0/sheets \
        -H "Authorization: Bearer ACCESS_TOKEN" \
        -H "Content-Type: application/json" \
        -X POST \
        -d '{"name":"newsheet",
             "columns":[
                 {"title":"Favorite","type":"CHECKBOX","symbol":"STAR"}, 
                 {"title":"Primary Column", "primary":true,"type":"TEXT_NUMBER"}, 
                 {"title":"Status", "type":"PICKLIST", "options":["Not Started","Started","Completed"]}]}'
        """
        result = await self.request(self.get_url(),
                                  method="POST", data=data)
        try:
            self._object_id = result['result']['id']
            self._data = result
        except KeyError as e:
            logging.exception("Can't create sheet")
        return self._data
        
    def to_dict():
        return self._data
