import json

import asyncio
import aiohttp_jinja2
import jinja2

from aiohttp import web

from boxcomtools.smartsheet.client import Client as SmartsheetClient
from .settings import (SMARTSHEET_CLIENT_ID,
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
aiohttp_jinja2.setup(app, loader=jinja2.FileSystemLoader(TEMPLATES))


async def smartsheet(request):
    client = SmartsheetClient(SMARTSHEET_CLIENT_ID, SMARTSHEET_CLIENT_SECRET)
    auth_url = client.auth_url
    return web.HTTPFound(auth_url)


@aiohttp_jinja2.template('base.html')
async def auth_smartsheet(request):
    _args = request.GET
    code = _args.get('code')
    print(code)
    client = SmartsheetClient(SMARTSHEET_CLIENT_ID, SMARTSHEET_CLIENT_SECRET)
    access_token, refresh_token = await client.authenticate(code)

    print(access_token)
    lists = await client.list_sheets(access_token)
    return custom_result([x.__dict__ for x in lists][0])


app.router.add_route("GET", '/', smartsheet)
app.router.add_route("GET", '/api/oauth/smartsheet', auth_smartsheet)


if __name__ == "__main__":
    web.run_app(app)
