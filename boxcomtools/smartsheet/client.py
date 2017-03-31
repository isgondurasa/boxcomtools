import hashlib
import json

import logging

from urllib.parse import urlencode

import aiohttp

from boxcomtools.base.config import SmartsheetConfig as Config
from boxcomtools.base.base_client import BaseClient
from boxcomtools.base.exceptions import NoAccessTokenException

from boxcomtools.smartsheet.sheets import Sheets


class Client(BaseClient, Config):

    def __init__(self, client_id, client_secret, access_token=None, refresh_token=None):

        super(Client, self).__init__(client_id,
                                     client_secret,
                                     access_token,
                                     refresh_token)

        self.state = Config.state
        self.scopes = ",".join(Config.scopes)

    @property
    def url_params(self):
        return {
            'response_type': 'code',
            'client_id': self._client_id,
            'scope': self.scopes,
            'state': self.state
        }
        
    @property
    def auth_url(self):
        return "%s?%s" % (Config.auth_endpoint,
                          urlencode(self.url_params))

    def get_token_url(self, body):
        return "%s?%s" % (self.token_obtaining_endpoint,
                          urlencode(body))
    
    async def authenticate(self, code):
        body = Config.token_obtaining_body
        body['client_id'] = self._client_id
        body['code'] = code

        _hash = "%s|%s" % (self._client_secret, code)
        body['hash'] = hashlib.sha256(_hash.encode("utf-8")).hexdigest()
        url = self.get_token_url(body)
        return await self._authenticate(url)
                
    # async def _request(self, access_token, method='get', resource='sheets', **params):
    #     """
    #     base request method
    #     """
    #     url = "%s%s" % (Config.request_url, resource)


        
    #     async with aiohttp.ClientSession() as session:
    #         async with getattr(session, method)\
    #             (url,
    #              headers=self.get_headers(access_token),
    #              data=json.dumps(params)) as resp:
    #             return await resp.text()
    #     raise Exception

    async def sheets(self):
        """
        returns a list of sheets in current users scope
        """

        sheets = Sheets(self)
        return await sheets.get()
        
        # res = await self._request(self._access_token)
        # sheets = []
        # try:
        #     res = json.loads(res)
        #     sheets = res['data']
        # except (ValueError, KeyError):
        #     logging.exception("Error in ")

    async def sheet(self, sheet_id=None):
        sheet = Sheet(self, sheet_id)
        return await sheet.get()
