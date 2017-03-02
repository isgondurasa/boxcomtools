import hashlib
import json

from urllib.parse import urlencode

import aiohttp
from boxcomtools.config import SmartsheetConfig as Config
from boxcomtools.exceptions import (NoClientKeyDefined,
                                    NoAuthCodeDefined,
                                    NoAccessTokenException)



class SmartsheetObject:

    def get(self):
        raise NotImplementedError

    def set(self, o):
        raise NotImplementedError

    def delete(self, o):
        raise NotImplementedError

    def update(self, o):
        raise NotImplementedError

    def to_json(self):
        return json.dumps(self.to_dict())

    def to_dict(self):
        return self.__dict__

    
class Sheet(SmartsheetObject):

    def __init__(self, o):
        self._base_object = o

        if isinstance(o, dict):
            for k, v in o.items():
                setattr(self, k, v)
                
class Client:

    def __init__(self, client_id, client_secret, access_token=None, refresh_token=None):

        if not client_id:
            raise NoClientKeyDefined("No Client ID")

        if not client_secret:
            raise NoClientKeyDefined("No Client Secret key")
        
        self.auth_url_t = """
            %(auth_endpoint)s?response_type=code&client_id=%(client_id)s&scope=%(scopes)s&state=%(state)s
        """
        self.client_id = client_id
        self.client_secret = client_secret

        self.access_token = access_token
        self.refresh_token = refresh_token
        
    @property
    def auth_url(self):
        return self.auth_url_t % dict(auth_endpoint=Config.auth_endpoint,
                                      client_id=self.client_id,
                                      scopes=" ".join(Config.scopes),
                                      state=Config.state)

    async def authorize(self, code):
        body = Config.token_obtaining_body
        body['client_id'] = self.client_id
        body['code'] = code

        import hashlib

        _hash = "%s|%s" % (self.client_secret, code)
        body['hash'] = hashlib.sha256(_hash.encode("utf-8")).hexdigest()

        headers = {
            'Content-Type': 'application/x-www-form-urlencoded'
        }
        url = Config.token_obtaining_endpoint + "?" + urlencode(body)
        
        async with aiohttp.ClientSession() as session:
            async with session.post(url,
                                    headers=headers,
                                    data=json.dumps(body)) as resp:
                body = await resp.text()
                try:
                    body = json.loads(body)

                    self.access_token = body.get('access_token')
                    self.refresh_token = body.get('refresh_token')
                    return self.access_token, self.refresh_token
                           
                except Exception as e:
                    print(e)
                    raise

    async def _request(self, access_token, method='get', resource='sheets', **params):
        """
        base request method
        """
        url = "%s%s" % (Config.request_url, resource)
        headers = {
            "Authorization": "Bearer " + access_token,
            "Content-Type": "application/json"
        }

        async with aiohttp.ClientSession() as session:
            async with getattr(session, method)(url,
                                                headers=headers,
                                                data=json.dumps(params)) as resp:
                return await resp.text()
        raise Exception

    async def list_sheets(self, access_token=None):
        """
        returns a list of sheets in current users scope
        """
        if not access_token:
            access_token = self.access_token
        
        if not access_token:
            raise NoAccessTokenException("No Access Token Defined")
        
        res = await self._request(access_token)
        try:
            res = json.loads(res)
            sheet_o_list = []
            sheets = res['data']
            for sheet in sheets:
                sheet_o_list.append(Sheet(sheet))
            return sheet_o_list
        except KeyError:
            raise
        except Exception:
            raise
        
        
if __name__ == "__main__":

    params = dict(
        test1='test_value_1',
        test2='test_value_2',
        test3='test_value_3',
        test4='test_value_4'
    )
    
    s = Sheet(params)
    assert s.test4 == 'test_value_4'
