import json
import logging

import asyncio
import aiohttp_jinja2
from aiohttp import web

import jinja2

from boxcomtools.box.client import Client
from .settings import BOX_CLIENT_ID, BOX_CLIENT_SECRET, TEMPLATES


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


def box(request):
    cli = Client(BOX_CLIENT_ID, BOX_CLIENT_SECRET)
    return web.HTTPFound(cli.auth_url)


@aiohttp_jinja2.template('base.html')
async def auth_box(request):
    _args = request.GET    
    code = _args.get("code")
    client = Client(BOX_CLIENT_ID, BOX_CLIENT_SECRET)

    access_token, refresh_token = await client.authenticate(code)
    logging.info("Access token is: %s" % access_token)
    logging.info("Refresh token is: %s" % refresh_token)
    folder = client.folder()
    folder_info = await folder.get()

    files = await folder.files
    for fi in files:
        data = await fi.get()

    for fi in files:
        m = await fi.get_metadata()
        print(m)
        
    return custom_result(folder_info)


app.router.add_route("GET", '/', box)
app.router.add_route("GET", '/api/oauth/login', auth_box)

if __name__ == "__main__":
    web.run_app(app)
