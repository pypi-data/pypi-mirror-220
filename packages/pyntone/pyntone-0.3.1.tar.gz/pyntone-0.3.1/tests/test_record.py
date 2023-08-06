import os.path
from os import environ as env
from uuid import uuid4

import dotenv
import pytest
from pyntone import KintoneRestAPIClient, ApiTokenAuth
from pyntone.types.record import RecordForParameter


@pytest.fixture(autouse=True, scope='session')
def load_env():
    if os.path.exists('.env'):
        dotenv.load_dotenv()


@pytest.fixture(autouse=True)
def client():
    auth = ApiTokenAuth(api_token=env['API_TOKEN'])
    client = KintoneRestAPIClient(base_url=env['BASE_URL'], auth=auth)
    return client


def test_add_record(client):
    add_record = {
        'column1': {'value': str(uuid4())},
        'column2': {'value': 'world'},
    }
    result = client.record.add_record(env['APP_ID'], add_record)
    assert result.get('id') is not None
    assert result.get('revision') is not None


def test_get_record(client):
    value = str(uuid4())
    add_record = {'column1': {'value': value}, 'column2': {'value': 'world'}}
    result = client.record.add_record(env['APP_ID'], add_record)
    resp = client.record.get_record(env['APP_ID'], result['id'])
    assert resp['record']['column1']['value'] == value
    assert resp['record']['column2']['value'] == 'world'


def test_update_record(client):
    add_record = {'column1': {'value': str(uuid4())}, 'column2': {'value': 'world'}}
    add_result = client.record.add_record(env['APP_ID'], add_record)
    update_record = {'column1': {'value': str(uuid4())}}
    update_result = client.record.update_record(
        1,
        record_id=add_result['id'],
        record=update_record,
        revision=add_result['revision'],
    )
    assert update_result.get('revision') is not None


def test_upsert_record(client):
    record = {'column2': {'value': 'upsert'}}
    update_key = {'field': 'column1', 'value': str(uuid4())}
    client.record.upsert_record(env['APP_ID'], update_key, record)


def test_get_all_records_with_cursor(client):
    client.record.get_all_records_with_cursor(env['APP_ID'])
    assert True


def test_add_all_records(client):
    add_records_num = 400
    add_records = [
        {'column1': {'value': str(uuid4())}, 'column2': {'value': 'world'}}
        for _ in range(add_records_num)
    ]
    results = client.record.add_all_records(env['APP_ID'], add_records)
    assert len(results['records']) == add_records_num


def test_update_all_records(client):
    add_records_num = 400
    add_records = [
        {'column1': {'value': str(uuid4())}, 'column2': {'value': 'world'}}
        for _ in range(add_records_num)
    ]
    results = client.record.add_all_records(env['APP_ID'], add_records)

    update_records = []
    for i in results['records']:
        update_records.append(
            {
                'id': i['id'],
                'record': {
                    'column1': {'value': str(uuid4())},
                    'column2': {'value': 'fuga'},
                },
                'revision': i['revision'],
            }
        )
    results = client.record.update_all_records(env['APP_ID'], update_records)
    assert len(results['records']) == add_records_num


def test_delete_all_reocrds(client):
    add_records_num = 400
    add_records = [
        {'column1': {'value': str(uuid4())}, 'column2': {'value': 'world'}}
        for _ in range(add_records_num)
    ]
    results = client.record.add_all_records(env['APP_ID'], add_records)

    delete_records = []
    for i in results['records']:
        delete_records.append(
            {
                'id': i['id'],
                # 'revision': i['revision']
            }
        )
    results = client.record.delete_all_reocrds(env['APP_ID'], delete_records)
    assert results == {}


def test_add_record_comment(client):
    add_record = {'column1': {'value': str(uuid4())}, 'column2': {'value': 'world'}}
    add_record_result = client.record.add_record(env['APP_ID'], add_record)
    add_comment = {'text': 'test comment'}
    add_comment_result = client.record.add_record_comment(
        env['APP_ID'], add_record_result.get('id'), add_comment
    )
    assert add_comment_result.get('id') is not None


def test_delete_record_comment(client):
    add_record = {
        'column1': {'value': str(uuid4())},
    }
    add_record_result = client.record.add_record(env['APP_ID'], add_record)
    add_comment = {'text': 'test comment'}
    add_comment_result = client.record.add_record_comment(
        env['APP_ID'], add_record_result['id'], add_comment
    )
    delete_comment_result = client.record.delete_record_comment(
        env['APP_ID'], add_record_result['id'], add_comment_result['id']
    )
    assert delete_comment_result == {}


def test_get_record_comments(client):
    add_record = {
        'column1': {'value': str(uuid4())},
    }
    add_record_result = client.record.add_record(env['APP_ID'], add_record)
    add_comment = {'text': 'test comment'}
    add_comment_result = client.record.add_record_comment(
        env['APP_ID'], add_record_result['id'], add_comment
    )
    get_comment_result = client.record.get_record_comments(
        env['APP_ID'], add_record_result['id']
    )
    assert get_comment_result['comments'][0]['text'] == 'test comment '


def test_update_record_assigness(client):
    add_record = {
        'column1': {'value': str(uuid4())},
    }
    add_record_result = client.record.add_record(env['APP_ID'], add_record)
    result = client.record.update_record_assigness(
        env['APP_ID'], add_record_result['id'], ['testuser']
    )
    assert result.get('revision') is not None


def test_update_record_status(client):
    add_record = {
        'column1': {'value': str(uuid4())},
    }
    add_record_result = client.record.add_record(env['APP_ID'], add_record)
    result = client.record.update_record_status(
        env['APP_ID'], add_record_result['id'], '処理開始'
    )
    assert result.get('revision') is not None
