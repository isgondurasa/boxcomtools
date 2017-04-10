import json

import asyncio

import jinja2
import aiohttp_jinja2

from aiohttp import web

from boxcomtools.smartsheet.client import Client as SmartsheetClient
from boxcomtools.smartsheet.sheet import Sheet
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
    client = SmartsheetClient(SMARTSHEET_CLIENT_ID, SMARTSHEET_CLIENT_SECRET)
    access_token, refresh_token = await client.authenticate(code)
    
    sheets = await client.sheets()

    for s in sheets:
        await s.get()

    sheet = sheets[-1]
    print(sheet.__dict__)
    
    rows = [
        {'col1': 'test_line_1', 'col2': 'test_line_1', 'col3': 'one'},
        {'col1': 'test_line_2', 'col2': 'test_line_2', 'col3': 'two'},
        {'col1': 'test_line_3', 'col2': 'test_line_3', 'col3': 'three'},
    ]
    
    res = await sheet.add_rows(rows)
    print(res)

    return custom_result(sheets[-1].__dict__)


app.router.add_route("GET", '/', smartsheet)
app.router.add_route("GET", '/api/oauth/smartsheet', auth_smartsheet)


if __name__ == "__main__":
    web.run_app(app)
