"""
General fixtures for application testing.
"""
import pytest
import aiohttp

from boxcomtools.box.client import Client as BoxClient
from boxcomtools.smartsheet.client import Client as SmartsheetClient
from boxcomtools.base.base_object import BaseObject


@pytest.fixture
def client(loop, test_client):
    app = aiohttp.web.Application(loop=loop)
    return loop.run_until_complete(test_client(app))


@pytest.fixture(scope="function", autouse=True)
def mock_box_auth(monkeypatch):
    async def auth(code, *args):
        return ('access', 'refresh')
    
    monkeypatch.setattr(BoxClient, 'authenticate', auth)
    monkeypatch.setattr(SmartsheetClient, 'authenticate', auth)


@pytest.fixture(scope="function", autouse=False)
def mock_base_response(monkeypatch):
    async def response(*args, **Kwargs):
        return {'response': 'ok', 'item_collection': {"entries": []}}
    monkeypatch.setattr(BaseObject, 'request', response)

@pytest.fixture(scope="function", autouse=False)
def mock_box_files_response(monkeypatch):
    async def get_base_file(*args, **kwargs):
        return {
            'name': 'test_file',
            'type': 'test',
            'id': 'test_file_id'
        }
    monkeypatch.setattr(BaseObject, 'request', get_base_file)
