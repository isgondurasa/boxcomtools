from boxcomtools.box import Client

from boxcomtools.smartsheet import Client as SmartsheetClient

import asyncio
import json

from aiohttp import web
from settings import (BOX_CLIENT_ID, BOX_CLIENT_SECRET,
                      SMARTSHEET_CLIENT_ID, SMARTSHEET_CLIENT_SECRET)


import aiohttp_jinja2
import jinja2


def box(request):
    cli = Client(BOX_CLIENT_ID, BOX_CLIENT_SECRET, callback=store_tokens)
    auth_url, csrf_token = cli.auth_url
    return redirect(auth_url)


async def smartsheet(request):
    cli = SmartsheetClient(SMARTSHEET_CLIENT_ID, SMARTSHEET_CLIENT_SECRET)
    auth_url = cli.auth_url
    print(auth_url)
    return web.HTTPFound(auth_url)

@aiohttp_jinja2.template('index.html')
async def auth_smartsheet(request):
    import ipdb; ipdb.set_trace()
    _args = request.GET
    code = _args.get('code')
    client = SmartsheetClient(SMARTSHEET_CLIENT_ID, SMARTSHEET_CLIENT_SECRET)
    res = await client.authorize(code)
    return locals()
    

@aiohttp_jinja2.template('index.html')
async def auth_box(request):

    _args = request.args
    code, state = _args.get("code"), _args.get("state")

    client = Client(BOX_CLIENT_ID, BOX_CLIENT_SECRET, callback=store_tokens)
    tokens = client.authenticate(code)
    access_token, refresh_token = tokens
    
    user = None
    with client as cli:
        user = cli.user().get().__dict__
        print(user)

    params = {
        'access_token': access_token,
        'refresh_token': refresh_token,
        'current_user': user
    }
        
    return params

def make_app(loop=None):
    app = web.Application(loop=loop)
    app.router.add_route("GET", '/smartsheet', smartsheet)
    app.router.add_route("GET", '/api/oauth/smartsheet', auth_smartsheet)

    app.router.add_route("GET", '/box', box)
    app.router.add_route("GET", '/api/oauth/box', auth_smartsheet)

    return app

app = make_app()

aiohttp_jinja2.setup(
    app, loader=jinja2.PackageLoader('templates'))

if __name__ == "__main__":
    web.run_app(app)
