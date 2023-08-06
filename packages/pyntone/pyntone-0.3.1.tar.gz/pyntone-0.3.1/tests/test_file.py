import io
import os.path
from os import environ as env
from uuid import uuid4

import dotenv
import pytest

from pyntone import ApiTokenAuth, KintoneRestAPIClient


@pytest.fixture(autouse=True, scope='session')
def load_env():
    if os.path.exists('.env'):
        dotenv.load_dotenv()


@pytest.fixture(autouse=True)
def client():
    auth = ApiTokenAuth(api_token=env['API_TOKEN'])
    client = KintoneRestAPIClient(base_url=env['BASE_URL'], auth=auth)
    return client


def test_upload_file(client):
    data = io.StringIO('hello')
    res = client.file.upload_file({'name': 'sample.txt', 'data': data})
    assert res.get('fileKey') is not None
    add_record = {
        'column1': {'value': str(uuid4())},
        'column2': {'value': 'world'},
        'file': {
            'value': [
                {
                    'fileKey': res['fileKey'],
                }
            ]
        },
    }
    result = client.record.add_record(env['APP_ID'], add_record)
    assert result.get('id') is not None
    assert result.get('revision') is not None


def test_download_file(client):
    data = io.StringIO('hello')
    res = client.file.upload_file({'name': 'sample.txt', 'data': data})
    add_record = {
        'column1': {'value': str(uuid4())},
        'column2': {'value': 'world'},
        'file': {
            'value': [
                {
                    'fileKey': res['fileKey'],
                }
            ]
        },
    }
    result = client.record.add_record(env['APP_ID'], add_record)
    res = client.record.get_record(env['APP_ID'], result['id'])
    client.file.download_file(res['record']['file']['value'][0]['fileKey'])
