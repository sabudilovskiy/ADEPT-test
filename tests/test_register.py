from datetime import datetime

import pytest

from testsuite.databases import pgsql


@pytest.mark.now('2024-03-30 05:00:00.000 +0300')
async def test_ok(service_client, todo_db):
    credentials = {
        'login': 'another_login',
        'password': 'another_password'
    }
    response = await service_client.post(
        '/register',
        json=credentials,
    )
    assert response.status == 200
    response_token_id = response.json()['token']
    user_id, login, password = todo_db.get_user_by_login('another_login')
    assert password == 'another_password'
    token_id, _, due_date = todo_db.get_token_by_user_id(user_id)
    assert token_id == response_token_id
    expeced_due_date = datetime.strptime(
        '2024-03-30 06:00:00.000 +0300',
        "%Y-%m-%d %H:%M:%S.%f %z")
    assert due_date == expeced_due_date


@pytest.mark.pgsql('todo_db',
                   files=[
                       'init_data_user.sql'
                   ])
async def test_used_credentials(service_client, todo_db):
    credentials = {
        'login': 'some_login',
        'password': 'another_password'
    }
    response = await service_client.post(
        '/register',
        json=credentials,
    )
    assert response.status == 400
    assert response.json()['error_code'] == 'username_busy'
    assert response.json()['message'] == 'Username is busy. Use another'
