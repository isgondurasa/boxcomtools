# file.py
from boxcomtools.base.base_object import BaseObject
from boxcomtools.box.metadata import Metadata

from boxcomtools.base.config import BoxConfig

class File(BaseObject, BoxConfig):
    """
    file API endpoint
    """
    __resource__ = "files"
    
    def __init__(self, session, object_id=None, name=""):
        super(File, self).__init__(session, object_id)
        
        self._metadata = Metadata(session, object_id)
        self._cached_metadata = None
        self._name = name
        self._data = None

    async def get(self):
        """
        curl https://api.box.com/2.0/files/FILE_ID
        -H "Authorization: Bearer ACCESS_TOKEN"
        """
        self._data = await self.request(self.get_url())
        return self._data

    async def get_metadata(self):
        self._cached_metadata = await self._metadata.get()
        return self._cached_metadata
