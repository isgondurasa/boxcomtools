# file_version.py

from boxcomtools.base.base_object import BaseObject
from boxcomtools.base.config import BoxConfig


class FileVersion(BaseObject, BoxConfig):
    """
    File version API endpoint
    """
    __resource__ = "versions"

    def get_url(self):
        return self.request_url + 'files/%s/%s' % (self.id,
                                                   self.__resource__)
