# box.com
import logging

from boxcomtools.base.base_client import BaseClient
from boxcomtools.base.config import BoxConfig as Config

from boxcomtools.box.file import File
from boxcomtools.box.folder import Folder


class Client(BaseClient, Config):

    def __init__(self, client_id, client_secret,
                 access_token=None, refresh_token=None):
        super(Client, self).__init__(client_id, client_secret,
                                     access_token, refresh_token)

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
