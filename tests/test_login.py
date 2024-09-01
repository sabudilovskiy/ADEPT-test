import pytest

from testsuite.databases import pgsql


# Start the tests via `make test-debug` or `make test-release`

@pytest.mark.pgsql('todo_db',
                   files=[
                       'init_data_user.sql'
                   ])
@pytest.mark.now('2024-03-30 05:00:00.000 +0300')
async def test_old_token(service_client):
    credentials = {
        'login': 'some_login',
        'password': 'some_password'
    }
    response = await service_client.post(
        '/login',
        json=credentials,
    )
    assert response.status == 200
    assert response.json()['token'] == 'd9ae85b8-6cc5-4e17-a857-a031277113c7'

@pytest.mark.pgsql('todo_db',
                   files=[
                       'init_data_user.sql'
                   ])
@pytest.mark.now('2024-03-30 07:00:00.000 +0300')
async def test_new_token(service_client):
    credentials = {
        'login': 'some_login',
        'password': 'some_password'
    }
    response = await service_client.post(
        '/login',
        json=credentials,
    )
    assert response.status == 200
    assert response.json()['token'] != 'd9ae85b8-6cc5-4e17-a857-a031277113c7'


@pytest.mark.pgsql('todo_db',
                   files=[
                       'init_data_user.sql'
                   ])
async def test_invalid_password(service_client):
    credentials = {
        'login': 'some_login',
        'password': 'invalid_password'
    }
    response = await service_client.post(
        '/login',
        json=credentials,
    )
    assert response.status == 400
    assert response.json()['error_code'] == 'invalid_credentials'
    assert response.json()['message'] == 'Invalid login or password'


async def test_invalid_login(service_client):
    credentials = {
        'login': 'invalid_login',
        'password': 'invalid_password'
    }
    response = await service_client.post(
        '/login',
        json=credentials,
    )
    assert response.status == 400
    assert response.json()['error_code'] == 'invalid_credentials'
    assert response.json()['message'] == 'Invalid login or password'
