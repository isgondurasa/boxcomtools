import pytest
from boxcomtools.base.base_object import BaseObject
from boxcomtools.box.client import Client
from boxcomtools.box.file import File
from boxcomtools.box.metadata import Metadata
from boxcomtools.box.template import Template

from .utils import get_auth_params


@pytest.mark.gen_test
async def test_box_auth(client, monkeypatch):
    client = Client("id", 'secret')
    auth_url = client.auth_url
    assert auth_url

    a_token, r_token = await client.authenticate("code")
    tokens = a_token, r_token

    assert a_token == 'access'
    assert r_token == 'refresh'


@pytest.mark.gen_test
@pytest.mark.usefixtures('mock_base_response')
async def test_box_folder(client, monkeypatch):
    client = Client(**get_auth_params())
    folder = client.folder()
    folder = await folder.get()
    assert folder['response'] == 'ok'


@pytest.mark.gen_test
@pytest.mark.usefixtures('mock_box_files_response')
async def test_box_client_file(client, monkeypatch):
    client = Client(**get_auth_params())
    f = client.file()
    f = await f.get()
    assert f['id'] == 'test_file_id'


@pytest.mark.gen_test
async def test_box_file_metadata(client, monkeypatch):
    async def get_metadata(*args, **kwargs):
        return {
            'entries': [{
                'key_1': 'field_1',
                'key_2': 'field_2'
            }]
        }
    client = Client(**get_auth_params())
    object_id = '5000948880'

    f = File(client, object_id)
    monkeypatch.setattr(BaseObject, 'request', get_metadata)
    m = await f.get_metadata()
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


@pytest.mark.gen_test
def test_template_get_url_template_name():
    template_name = 'test_template'
    t = Template("session", template_name)
    url = t.get_url()

    assert template_name in url
    assert url == 'https://api.box.com/2.0/metadata_templates/enterprise/test_template/schema'


@pytest.mark.gen_test
def test_template_get_url_no_template_name():
    t = Template("session")

    url = t.get_url()

    assert url == 'https://api.box.com/2.0/metadata_templates/enterprise/'
