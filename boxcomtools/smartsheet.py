
class NoKeyDefined(Exception):
    pass


class Config:
    auth_endpoint = "https://app.smartsheet.com/b/authorize"
    redirect_url = "http://localhost:5000/api/oauth/smartsheet"
    scopes = ("READ_SHEETS", "WRITE_SHEETS", "DELETE_SHEETS", "CREATE_SHEETS", "SHARE_SHEETS")

class Client:


    def __init__(self, client_id, client_secret):

        if not client_id or not client_secret:
            raise NoKeyDefined
        
        self.auth_url_t = """
            %(auth_endpoint)s?response_type=code&client_id=%(client_id)s&scope=%(scopes)s&state=%(state)s
        """
        self.client_id = client_id
        self.client_secret=client_secret
        self.scopes = ""
        self.state = ""

    
