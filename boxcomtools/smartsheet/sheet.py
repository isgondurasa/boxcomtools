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
        self._cols = []
        self._rows = []

    def get_url(self):
        return super().get_url(self._object_id or None)

    async def get(self):
        result = await super().get()
        self._cols = result['result']['columns']
        for col in self._cols:
            self.__name_to_id[col['title']] = col['id']
        return result

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
        print(data)
        result = await self.request(self.get_url(),
                                    method="POST", data=data)
        print(result)
        self._data = result['result']
        try:
            self._object_id = self._data['id']
        except KeyError as e:
            logging.exception("Can't create sheet")

        self._cols = self._data['columns']

        for col in self._cols:
            self.__name_to_id[col['title']] = col['id']

        return self._data

    async def add_rows(self, rows):
        """
        rows = [{"key": "value"}]

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

        cells = []
        for row in rows:
            line = [{"columnId": self.__name_to_id[name],
                    "value": value} for name, value in row.items()]
            cells.append({
                'toTop': True,
                'cells': line
            })

        return await self.request(self.get_url() + '/rows',
                                  method='POST',
                                  data=cells)
        
    def to_dict(self):
        return self._data
