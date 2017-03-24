# file.py
import logging

from boxcomtools.base.base_object import BaseObject
from boxcomtools.box.file import File
from boxcomtools.base.config import BoxConfig as Config


class Folder(BaseObject, Config):
    """
    folder API endpoint
    """
    __resource__ = "folders"
    
    def __init__(self, session, object_id=None):
        super(Folder, self).__init__(session, object_id)
        self._object_id = object_id or "0"
        self._files = []
        self._data = {}

    async def get(self):
        """
        curl https://api.box.com/2.0/folders/FOLDER_ID \
        -H "Authorization: Bearer ACCESS_TOKEN" \
        """
        try:
            self._data = await self.request(self.get_url())
            self._attach_to_object(self._data)            
        except KeyError as e:
            logging.exception(e)
        return self._data

    @property
    async def files(self):

        if self._files:
            return self._files

        def to_objects(self):
            dic = self.item_collection['entries']
            return [
                File(self._session,
                     x['id']) for x in dic if x['type'] == 'file'
            ]
            
        if self.item_collection and 'entries' in self.item_collection:
            self._files = to_objects(self)
        else:
            data = await self.get()
            self._files = to_objects(self)
        return self._files
