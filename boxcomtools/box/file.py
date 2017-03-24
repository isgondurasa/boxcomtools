# file.py
from boxcomtools.base.base_object import BaseObject
from boxcomtools.box.metadata import Metadata

from boxcomtools.base.config import BoxConfig

class File(BaseObject):
    """
    file API endpoint
    """
    def __init__(self, session, object_id=None, name=""):
        super(File, self).__init__(session, object_id)
        
        self._metadata = Metadata(session, object_id)
        self._cached_metadata = None
        self._name = name
        self._data = None

    def get_url(self):
        """
        returns base url for file API endpoint
        """
        return BoxConfig.request_url + "files/%s" % self._object_id

    async def get(self, skip=0, page=10):
        """
        curl https://api.box.com/2.0/files/FILE_ID
        -H "Authorization: Bearer ACCESS_TOKEN"
        """
        self._data = await self.request(self.get_url())
        self._attach_to_object(self._data)
        return self._data

    @property
    async def metadata(self):
        if self._cached_metadata:
           return self._cached_metadata
       
        self._cached_metadata = await self._metadata.get()
        return self._cached_metadata
