# box_to_smartsheet.py
import sys
sys.path.append("..")

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
from boxcomtools.base.transfer_client import BoxToSmartsheet


from .settings import (BOX_CLIENT_ID,
                       BOX_CLIENT_SECRET,
                       SMARTSHEET_CLIENT_ID,
                       SMARTSHEET_CLIENT_SECRET,
                       TEMPLATES)


async def get_tokens_from_session(request):
    session = await get_session(request)
    return {
        'box_access_token': session.get('box_access_token'),
        'box_refresh_token': session.get('box_refresh_token'),
        'smartsheet_access_token': session.get('smartsheet_access_token'),
        'smartsheet_refresh_token': session.get('smartsheet_refresh_token')
    }


def custom_result(data):
    return {
        'data': data,
        'result': 'ok',
        'errors': []
    }


def make_app(loop=None):
    return web.Application(loop=loop)


app = make_app()
#fernet_key = fernet.Fernet.generate_key()
#print(fernet_key)
fernet_key = b'C_ATKLVqNkGUf1_BTp69pyE-K8dR1gV3MNoz-jIeDBU='
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

    return web.HTTPFound("/")


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
    return web.HTTPFound("/")

@aiohttp_jinja2.template('box_to_smartsheet.html')
async def index(request):
    response = {
        'box_auth': False,
        'sm_auth': False,
    }
    session = await get_session(request)
    
    box_access_token = session.get("box_access_token", "")
    box_refresh_token = session.get("box_refresh_token", "")
    if box_access_token:
        response['box_auth'] = True
        box_cli = BoxClient(BOX_CLIENT_ID, BOX_CLIENT_SECRET,
                            box_access_token, box_refresh_token)

        folder = box_cli.folder()
        finfo = await folder.get()
        response['folder'] = finfo['item_collection']['entries']

    sm_access_token = session.get('smartsheet_access_token')
    if sm_access_token:
        response['sm_auth'] = True
    return response


async def transfer_metadata(request):
    print ("transfer_metadata")
    tokens = await get_tokens_from_session(request)
    print(tokens)
    box_cli = BoxClient(BOX_CLIENT_ID, BOX_CLIENT_SECRET,
                        tokens['box_access_token'], tokens['box_refresh_token'])

    sm_cli = SmartsheetClient(SMARTSHEET_CLIENT_ID, SMARTSHEET_CLIENT_SECRET,
                              tokens['smartsheet_access_token'], tokens['smartsheet_refresh_token'])

    bts_cli = BoxToSmartsheet(box_cli, sm_cli)
    await bts_cli.transfer()
    return web.HTTPFound("/")

# sm_access_token = session.get('smartsheet_access_token')
# sm_refresh_token = session.get('smartsheet_refresh_token')


app.router.add_route("GET", "/", index)
app.router.add_route("GET", "/box", box)
app.router.add_route("GET", "/smartsheet", smartsheet)
app.router.add_route("GET", '/api/oauth/login', auth_box)
app.router.add_route("GET", "/api/oauth/smartsheet", auth_smartsheet)
app.router.add_route("GET", "/transfer_metadata", transfer_metadata)

if __name__ == "__main__":
    web.run_app(app)
