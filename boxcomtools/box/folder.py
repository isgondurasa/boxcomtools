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

    async def get(self):
        """
        curl https://api.box.com/2.0/folders/FOLDER_ID \
        -H "Authorization: Bearer ACCESS_TOKEN" \
        """
        url = "%s/%s" % (self.get_url(), self._object_id)
        self._data = await self.request(url)
        return self._data

    @property
    async def files(self):

        if self._files:
            return self._files

        def to_files(data):
            return [
                File(self._session,
                     x['id']) for x in data if x['type'] == 'file'
            ]

        if not self._data:
            await self.get()
        try:
            self._files = to_files(self._data['item_collection']['entries'])
        except KeyError:
            logging.exception("No item collection")
        
        return self._files
