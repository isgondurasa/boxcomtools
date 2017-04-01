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

        self.__name_to_id = {}
                
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
        except KeyError as e:
            logging.exception("Can't create sheet")
        self._data = result

        for col in result['result']:
            self.__name_to_id[result['result']['title']] = result['result']['id']
        return self._data

    def add_rows(self, rows):
        """
        curl https://api.smartsheet.com/2.0/sheets/{sheetId}/rows \
        -H "Authorization: Bearer ACCESS_TOKEN" \
        -H "Content-Type: application/json" \
        -X POST \
        -d '[{"toTop":true, 
              "cells": [ {"columnId": 7960873114331012, "value": true}, 
                         {"columnId": 642523719853956, "value": "Y", "strict": false} ] }]'
        """
        if not self._data:
            raise Exception("No column ids could be found")

        data = {
            'toTop': True,
            "cells"[
                {"columnId": self.__name_to_id[name],
                 "value": value} for name, value in row.items()
            ]
        }

        return await self.request(self.get_url('rows'),
                           method='POST', data=data)
        
    def to_dict():
        return self._data
