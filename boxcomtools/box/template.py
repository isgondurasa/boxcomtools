# template.py
import logging

from boxcomtools.base.base_object import BaseObject
from boxcomtools.base.config import BoxConfig

from urllib.parse import urljoin






class Template(BaseObject, BoxConfig):
    """
    Endpoint for metadata templates

    https://api.box.com/2.0/metadata_templates/{scope}/{template}/schema
    """
    __resource__ = "metadata_templates"
    __scope__ = "enterprise"

    def __init__(self, session, template_name=None):
        super(Template, self).__init__(session)
        self._template_name = template_name
    
    def get_url(self, create=False):

        if create:
            return urljoin(self.request_url, "%s/schema" % self.__resource__)
        
        url = urljoin(self.request_url, "%s/%s" % (self.__resource__, self.__scope__)) + "/"
        if self._template_name:
            url = urljoin(url, "%s/schema" % (self._template_name))
        return url
    
    async def get(self):
        """
        curl https://api.box.com/2.0/metadata_templates/enterprise/productInfo/schema
        if no template defined, returns all templates in enterprise scope
        """
        res =  await super().get()
        try:
            return res['entries']
        except KeyError as e:
            logging.exception(e)
            return []

    async def create(self, key, fields, name=None):
        """
        ref:
            https://docs.box.com/reference#create-metadata-schema

        curl https://api.box.com/2.0/metadata_templates/schema
        -H "Authorization: Bearer ACCESS_TOKEN" \
        -H "Content-Type: application/json" \
        -X POST \
        body:
            "templateKey"
            "scope"
            "displayName"
            "fields":
                "key"
                "type"
                "displayName"
        """

        if not name:
            name = key

        data = {
            'templateKey': key,
            'scope': self.__scope__,
            'displayName': name,
            'fields': fields
        }

        res = await self.request(self.get_url(create=True), method="POST", data=data)
        self._data = res
        self._template_name = key
        return res
