# file_version.py

from boxcomtools.base.base_object import BaseObject


class FileVersion(BaseObject, BoxConfig):
    """
    File version API endpoint   
    """
    __resource__ = "versions"


    def get_url(self):
        url = self.request_url + 'files/%s/%s' % (self.id,
                                                  self.__resource__)

    async def get(self):
        """
        curl https://api.box.com/2.0/files/FILE_ID/versions \
        -H "Authorization: Bearer ACCESS_TOKEN"
        """
