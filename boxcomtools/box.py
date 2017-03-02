# box.com

from boxsdk import OAuth2, Client as BoxSDKClient
from boxsdk.exception import BoxOAuthException

__all__ = ('Client',)

class BaseOauthClient:
    pass

class AsyncBoxObject:

    def __init__(self, connection):
        self._connection = connection
    
    async def create(self):
        raise NotImplementedError

    async def get(self, id):
        raise NotImplementedError

    async def get_all(self):
        raise NotImplementedError

    
class Metadata(AsyncBoxObject):

    async def get(self, f_id, scope='enterprise'):
        url = self._connection.get_url("files/%d/metadata/" % f_id)
        response = self._connection.make_request(method="GET", url=url)
        return response.json

    async def set(self, f_id, items, scope='enterprise', **kwargs):
        pass

    
class Client(BaseOauthClient):
    
    def __init__(self, client_id, client_secret,
                 access_token=None, refresh_token=None, callback=None):
        self.client_id = client_id
        self.client_secret = client_secret
        self.access_token = access_token
        self.refresh_token = refresh_token
        self.callback = callback

    def __enter__(self):

        def store_tokens(access_token, refresh_token):
            self.access_token = access_token
            self.refresh_token = refresh_token

        oauth = OAuth2(client_id=self.client_id,
                       client_secret=self.client_secret,
                       access_token=self.access_token,
                       refresh_token=self.refresh_token,
                       store_tokens=store_tokens and self.callback)

        return BoxSDKClient(oauth)

    def __exit__(self, client_id, client_secret, access_token=None, refresh_token=None, callback=None):
        self.access_token = None
        self.refresh_token = None
        if callback:
            callback(self.access_token, self.refresh_token)

    @property
    def auth_url(self):
        """
        return: auth_url, csrf_token
        """
        return OAuth2(client_id=self.client_id,
                      client_secret=self.client_secret).get_authorization_url("")


    def authenticate(self, auth_code):
        """
        return access_token, refresh_token
        """
        tokens = OAuth2(client_id=self.client_id,
                        client_secret=self.client_secret).authenticate(auth_code)
        self.access_token, self.refresh_token = tokens
        return tokens
