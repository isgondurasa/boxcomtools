
class NoClientKeyDefined(Exception):
    pass


class NoAuthCodeDefined(Exception):
    pass


class Config:
    auth_endpoint = "https://app.smartsheet.com/b/authorize"
    token_obtaining_endpoint = "https://api.smartsheet.com/2.0/token"    
    token_obtaining_body = {
        'grant_type': 'authorization_code',
        'client_id': None,
        'code': None,
        'redirect_uri': "http://localhost:8080/api/oauth/smartsheet",
        'hash': '123123'
    }
    
    redirect_url = "http://localhost:8080/api/oauth/smartsheet"
    #scopes = ("READ_SHEETS", "WRITE_SHEETS", "DELETE_SHEETS", "CREATE_SHEETS", "SHARE_SHEETS")
    scopes = ("READ_SHEETS", "CREATE_SHEETS")
    state = "PREPARE"

    
class Client:

    def __init__(self, client_id, client_secret):

        if not client_id:
            raise NoClientKeyDefined("No Client ID")

        if not client_secret:
            raise NoClientKeyDefined("No Client Secret key")
        
        self.auth_url_t = """
            %(auth_endpoint)s?response_type=code&client_id=%(client_id)s&scope=%(scopes)s&state=%(state)s
        """
        self.client_id = client_id
        self.client_secret = client_secret

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

        _hash = hashlib.sha256((self.client_secret + code).encode("utf-8")).hexdigest()
        body['hash'] = _hash
        
        headers = {
            'Content-Type': 'application/x-www-form-urlencoded'
        }

        import json
        import aiohttp

        async with aiohttp.ClientSession() as session:
            async with session.post(Config.token_obtaining_endpoint,
                                    headers=headers,
                                    data=json.dumps(body)) as resp:
                print(resp.status)
                body = await resp.text()
                return body
        
