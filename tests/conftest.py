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
            "type": "file",
            "id": "12345",
            "file_version": {
                "type": "file_version",
                "id": "26261748416",
                "sha1": "134b65991ed521fcfe4724b7d814ab8ded5185dc"
            },
            "sequence_id": "3",
            "etag": "3",
            "sha1": "134b65991ed521fcfe4724b7d814ab8ded5185dc",
            "name": "tigers.jpeg",
            "description": "a picture of tigers",
            "size": 629644,
            "path_collection": {
                "total_count": 2,
                "entries": [
                    {
                        "type": "folder",
                        "id": "0",
                        "sequence_id": None,
                        "etag": None,
                        "name": "All Files"
                    },
                    {
                        "type": "folder",
                        "id": "11446498",
                        "sequence_id": "1",
                        "etag": "1",
                        "name": "Pictures"
                    }
                ]
            },
            "created_at": "2012-12-12T10:55:30-08:00",
            "modified_at": "2012-12-12T11:04:26-08:00",
            "created_by": {
                "type": "user",
                "id": "17738362",
                "name": "sean rose",
                "login": "sean@box.com"
            },
            "modified_by": {
                "type": "user",
                "id": "17738362",
                "name": "sean rose",
                "login": "sean@box.com"
            },
            "owned_by": {
                "type": "user",
                "id": "17738362",
                "name": "sean rose",
                "login": "sean@box.com"
            },
            "shared_link": {
                "url": "https://www.box.com/s/rh935iit6ewrmw0unyul",
                "download_url": "https://www.box.com/shared/static/rh935iit6ewrmw0unyul.jpeg",
                "vanity_url": None,
                "is_password_enabled": False,
                "unshared_at": None,
                "download_count": 0,
                "preview_count": 0,
                "access": "open",
                "permissions": {
                    "can_download": True,
                    "can_preview": True
                }
            },
            "parent": {
                "type": "folder",
                "id": "11446498",
                "sequence_id": "1",
                "etag": "1",
                "name": "Pictures"
            },
            "item_status": "active"
        }
    monkeypatch.setattr(BaseObject, 'request', get_base_file)
