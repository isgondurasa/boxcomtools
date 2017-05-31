# config.py
import os

env_get = os.environ.get


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

    redirect_url = env_get("SM_REDIRECT_URL", "http://localhost:8080/api/oauth/smartsheet")
    scopes = ("READ_SHEETS", "WRITE_SHEETS", "DELETE_SHEETS", "CREATE_SHEETS", "SHARE_SHEETS")
    state = "PREPARE"
    request_url = env_get("SM_REQUEST_URL", "https://api.smartsheet.com/2.0/")


class BoxConfig:
    auth_endpoint = env_get("BOX_AUTH_URL", "https://account.box.com/api/oauth2/authorize")
    token_endpoint = env_get("BOX_TOKEN_URL",
                             "https://api.box.com/oauth2/token")
    request_url = env_get("BOX_REQUEST_URL", "https://api.box.com/2.0/")
    redirect_url = env_get("BOX_REDIRECT_URL", "http://localhost:8080/api/oauth/login")

    token_obtaining_body = {
        'grant_type': 'authorization_code',
        'code': None,
        'client_id': None,
        'client_secret': None
    }
