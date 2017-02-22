# config.py


class SmartsheetConfig:
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
    scopes = ("READ_SHEETS", "WRITE_SHEETS", "DELETE_SHEETS", "CREATE_SHEETS", "SHARE_SHEETS")
    state = "PREPARE"

    request_url = "https://api.smartsheet.com/2.0/"
    
class BoxConfig:
    pass
