# box.com
import logging

from boxcomtools.base.base_client import BaseClient
from boxcomtools.base.config import BoxConfig as Config

from boxcomtools.box.file import File
from boxcomtools.box.folder import Folder
from boxcomtools.box.template import Template


class Client(BaseClient, Config):

    @property
    def url_params(self):
        return {
            'response_type': 'code',
            'client_id': self._client_id,
            'redirect_uri': '',
            'state': 'auth'
        }

    async def authenticate(self, code):
        """
        return access_token, refresh_token
        """
        body = self.token_obtaining_body
        body['code'] = code
        body['client_id'] = self._client_id
        body['client_secret'] = self._client_secret
        try:
            await self._authenticate(self.token_endpoint,
                                     self.auth_headers,
                                     body)
            return self.tokens
        except Exception as e:
            logging.exception(e)

    def file(self, object_id=None):
        return File(self, object_id)

    def folder(self, object_id=None):
        return Folder(self, object_id)

    def template(self, template_name=None):
        return Template(self, template_name)
