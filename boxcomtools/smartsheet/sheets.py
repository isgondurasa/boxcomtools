import logging

from boxcomtools.base.base_object import BaseObject
from boxcomtools.base.config import SmartsheetConfig
from boxcomtools.smartsheet.sheet import Sheet


class Sheets(BaseObject, SmartsheetConfig):
    __resource__ = "sheets"

    async def get(self):
        self._data = await self.request(self.get_url())
        try:
            self._data = self._data['data']

            
            return [Sheet(self._session,
                          s['id'],
                          **s) for s in self._data]
        except KeyError as e:
            logging.exception(e)
