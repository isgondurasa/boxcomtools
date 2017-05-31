# folder.py
import logging

from boxcomtools.base.base_object import BaseObject
from boxcomtools.box.file import File
from boxcomtools.base.config import BoxConfig as Config


class Folder(BaseObject, Config):
    """
    folder API endpoint
    """
    __resource__ = "folders"
    
    def __init__(self, session, object_id="0"):
        super(Folder, self).__init__(session, object_id)
        if not object_id:
            self._object_id = "0"
        self._files = []
        self._data = {}
        self._children = []

    async def get(self):
        """
        curl https://api.box.com/2.0/folders/FOLDER_ID \
        -H "Authorization: Bearer ACCESS_TOKEN" \
        """
        self._data = await self.request(self.get_url())

        print(self._data)
        
        try:
            self._children = self._data['item_collection']['entries']
        except KeyError:
            logging.exception("No children or bad response")
        return self._data

    @property
    def children(self):
        return self._children

    def __parse_to_files(self, files):
        return [
                File(self._session,
                     f['id']) for f in files if f['type'] == 'file'
        ]

    @property
    async def files(self):
        if not self._data:
            await self.get()
        return self.__parse_to_files(self._children)
