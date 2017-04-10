# box_to_smartsheet.py
import base64
import json

import jinja2
import aiohttp_jinja2

from aiohttp import web

from cryptography import fernet

from aiohttp_session import setup, get_session, session_middleware
from aiohttp_session.cookie_storage import EncryptedCookieStorage

from boxcomtools.base.transfer_client import BoxToSmartsheet
from boxcomtools.box.client import Client as BoxClient
from boxcomtools.smartsheet.client import Client as SmartsheetClient

from .settings import (BOX_CLIENT_ID,
                       BOX_CLIENT_SECRET,
                       SMARTSHEET_CLIENT_ID,
                       SMARTSHEET_CLIENT_SECRET,
                       TEMPLATES)



def custom_result(data):
    return {
        'data': data,
        'result': 'ok',
        'errors': []
    }


def make_app(loop=None):
    return web.Application(loop=loop)


app = make_app()
fernet_key = fernet.Fernet.generate_key()
secret_key = base64.urlsafe_b64decode(fernet_key)
setup(app, EncryptedCookieStorage(secret_key))

aiohttp_jinja2.setup(app, loader=jinja2.FileSystemLoader(TEMPLATES))


def box(request):
    cli = BoxClient(BOX_CLIENT_ID,
                    BOX_CLIENT_SECRET)
    return web.HTTPFound(cli.auth_url)


def smartsheet(request):
    cli = SmartsheetClient(SMARTSHEET_CLIENT_ID,
                           SMARTSHEET_CLIENT_SECRET)
    return web.HTTPFound(cli.auth_url)


@aiohttp_jinja2.template('box_to_smartsheet.html')
async def auth_box(request):
    _args = request.GET    
    code = _args.get("code")
    client = BoxClient(BOX_CLIENT_ID, BOX_CLIENT_SECRET)
    access_token, refresh_token = await client.authenticate(code)

    session = await get_session(request)
    session['box_access_token'] = access_token
    session['box_refresh_token'] = refresh_token
    
    return {'box_access_token': access_token,
            'box_refresh_token': refresh_token}


@aiohttp_jinja2.template('box_to_smartsheet.html')
async def auth_smartsheet(request):
    _args = request.GET    
    code = _args.get("code")
    client = SmartsheetClient(SMARTSHEET_CLIENT_ID,
                              SMARTSHEET_CLIENT_SECRET)
    access_token, refresh_token = await client.authenticate(code)

    session = await get_session(request)

    session['smartsheet_access_token'] = access_token
    session['smartseet_refresh_token'] = refresh_token

    box_access_token = session.get("box_access_token", "")
    box_refresh_token = session.get("box_refresh_token", "")

    return {'smartsheet_access_token': access_token,
            'smartsheet_refresh_token': refresh_token,
            'box_access_token': box_access_token,
            'box_refresh_token': box_refresh_token}

@aiohttp_jinja2.template('box_to_smartsheet.html')
def index(request):

    session = await get_session(request)
    
    return {}


app.router.add_route("GET", "/", index)
app.router.add_route("GET", "/box", box)
app.router.add_route("GET", "/smartsheet", smartsheet)
app.router.add_route("GET", '/api/oauth/login', auth_box)
app.router.add_route("GET", "/api/oauth/smartsheet", auth_smartsheet)


if __name__ == "__main__":
    web.run_app(app)
