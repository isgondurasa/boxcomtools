import pytest
from boxcomtools.base.base_object import BaseObject
from boxcomtools.box.client import Client
from boxcomtools.box.file import File
from boxcomtools.box.metadata import Metadata


from .utils import get_auth_params


@pytest.mark.gen_test
async def test_box_auth(client, monkeypatch):
    client = Client("id", 'secret')

    auth_url = client.auth_url
    assert auth_url

    async def auth(code, *args):
        return ('access_token', 'refresh_token')

    # code, state part
    monkeypatch.setattr(Client,
                        'authenticate',
                        auth)

    a_token, r_token = await client.authenticate("code")
    tokens = a_token, r_token

    assert a_token == 'access_token'
    assert r_token == 'refresh_token'
    

@pytest.mark.gen_test
async def test_box_folder(client, monkeypatch):

    client = Client(**get_auth_params())

    async def get_base_folder(*args, **Kwargs):
        return {'response': 'ok'}
    monkeypatch.setattr(BaseObject, 'request', get_base_folder)
    folder = await client.folder()
    folder = await folder.get()
    assert folder['response'] == 'ok'


@pytest.mark.gen_test
async def test_box_client_file(client, monkeypatch):
    client = Client(**get_auth_params())
    object_id = '5000948880'

    async def get_base_file(*args, **kwargs):
        return {
            'name': 'test_file',
            'type': 'test',
            'id': object_id
        }

    monkeypatch.setattr(BaseObject, 'request', get_base_file)
    f = await client.file()
    f = await f.get()
    assert f['id'] == object_id


@pytest.mark.gen_test
async def test_box_file_metadata(client, monkeypatch):
    async def get_metadata(*args, **kwargs):
        return [{
            'key_1': 'field_1',
            'key_2': 'field_2'
        }]
    client = Client(**get_auth_params())
    object_id = '5000948880'

    f = File(client, object_id)
    monkeypatch.setattr(BaseObject, 'request', get_metadata)
    m = await f.metadata
    assert len(m) == 1
    assert m[0]['key_1'] == 'field_1'

@pytest.mark.gen_test
async def test_box_file_template_metadata(client, monkeypatch):
    async def get_metadata(*args, **kwargs):
        return {
            'key_1': 'val_1',
            'key_2': 'val_2'
        }

    client = Client(**get_auth_params())
    object_id = 5000948880
    monkeypatch.setattr(BaseObject, 'request', get_metadata)
    m = Metadata(client, object_id)
    metadata = await m.get(template='test')

    assert metadata['key_1'] == 'val_1'
