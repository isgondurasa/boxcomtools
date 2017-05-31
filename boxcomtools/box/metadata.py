# metadata.py
from boxcomtools.base.base_object import BaseObject
from boxcomtools.base.config import BoxConfig


class Metadata(BaseObject):
    """
    metadata API endpoint
    """
    __scope__ = 'enterprise'
    __resource__ = "metadata"

    def get_url(self, template=""):
        url = BoxConfig.request_url + 'files/%s/metadata' % self.id
        if template:
            url += "/%s/%s" % (self.__scope__, template)
        return url

    def to_json(self):
        if not self._data:
            return {}

    async def get(self, template=""):
        """
        curl https://api.box.com/2.0/files/5010739061/metadata/enterprise/bandInfo \
        -H "Authorization: Bearer ACCESS_TOKEN"
        """
        self._data = await self.request(url=self.get_url(template))
        return self._data

    async def post(self, items, template):
        """
        TODO (sao): create 
        """
        if not template:
            raise AttributeError("No template defined")
        url = self.get_url(template)
        return await self.request(method="POST",
                                  data=items)

    async def delete(self, f_id):
        """
        TODO (sao): delete
        """

    async def put(self, ):
        """
        TODO (sao): delete
        """
