import hashlib
import json

from urllib.parse import urlencode

import aiohttp

from boxcomtools.base.config import SmartsheetConfig as Config
from boxcomtools.base.base_client import BaseClient
from boxcomtools.base.exceptions import NoAccessTokenException

from boxcomtools.smartsheet.sheet import Sheet


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
            'client_id': self.client_id,
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
        body['client_id'] = self.client_id
        body['code'] = code

        _hash = "%s|%s" % (self.client_secret, code)
        body['hash'] = hashlib.sha256(_hash.encode("utf-8")).hexdigest()

        headers = {
            'Content-Type': 'application/x-www-form-urlencoded'
        }
        url = self.get_token_url(body)
        
        return await self._authenticate(url, headers)
                
    async def _request(self, access_token, method='get', resource='sheets', **params):
        """
        base request method
        """
        url = "%s%s" % (Config.request_url, resource)

        async with aiohttp.ClientSession() as session:
            async with getattr(session, method)\
                (url,
                 headers=self.get_headers(access_token),
                 data=json.dumps(params)) as resp:
                return await resp.text()
        raise Exception

    async def list_sheets(self, access_token=None):
        """
        returns a list of sheets in current users scope
        """

        if not access_token and not hasattr(self, 'access_token'):
            raise NoAccessTokenException("No Access Token Defined")
        
        res = await self._request(access_token)
        try:
            res = json.loads(res)
            sheet_o_list = []
            sheets = res['data']
            for sheet in sheets:
                sheet_o_list.append(Sheet(sheet))
            return sheet_o_list
        except Exception:
            raise

    async def get_sheet(self, sheet_id=None):
        pass
