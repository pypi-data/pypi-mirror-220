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


def test_get_form_fields(client):
    result = client.app.get_form_fields(env['APP_ID'])
    assert result.get('revision') is not None
    assert result.get('properties') is not None


def test_add_form_fields(client):
    pass


def test_update_form_fields(client):
    pass


def test_delete_form_fields(client):
    pass


def test_get_form_layout(client):
    result = client.app.get_form_layout(env['APP_ID'])
    assert result.get('revision') is not None
    assert result.get('layout') is not None


def test_update_form_layout(client):
    pass


def test_get_views(client):
    result = client.app.get_views(env['APP_ID'])
    assert result.get('revision') is not None
    assert result.get('views') is not None


def test_update_views(client):
    pass


def test_get_app(client):
    result = client.app.get_app(env['APP_ID'])
    assert result.get('appId') is not None


def test_add_app(client):
    pass


def test_get_app_settings(client):
    pass


def test_update_app_settings(client):
    pass


def test_get_process_management(client):
    pass


def test_update_process_management(client):
    pass


def test_get_deploy_status(client):
    pass


def test_deploy_app(client):
    pass


def test_get_field_acl(client):
    pass


def test_update_field_acl(client):
    pass


def test_get_app_acl(client):
    pass


def test_update_app_acl(client):
    pass


def test_evaluate_records_acl(client):
    pass


def test_get_record_acl(client):
    pass


def test_update_record_acl(client):
    pass


def test_get_app_customize(client):
    pass


def test_update_app_customize(client):
    pass


def test_get_general_notifications(client):
    pass


def test_update_general_notifications(client):
    pass


def test_get_per_record_notifications(client):
    pass


def test_update_per_record_notifications(client):
    pass


def test_get_reminder_notifications(client):
    pass


def test_update_reminder_notifications(client):
    pass


def test_get_reports(client):
    pass


def test_update_reports(client):
    pass


def test_get_app_actions(client):
    pass


def test_update_app_actions(client):
    pass
