from datetime import datetime

import pytest

from testsuite.databases import pgsql


@pytest.mark.now('2024-03-30 05:00:00.000 +0300')
async def test_ok(service_client, objects_db):
    body = {
        "name": "Игорь",
        "coordinates": {
            "x": "0.132",
            "y": "1.15"
        },
        "type_name": "человек",
        "token_idempotency": "e7df97a2-278d-476a-98ca-3f31ef6cf5c8"
    }
    response = await service_client.post(
        '/object',
        json=credentials,
    )
    assert response.status == 200
    object_id = response.json()['object_id']
    object = objects_db.get_object_by_id(object_id)
    assert object.name == 'Игорь'
    assert object.coordinates.x == '0.132'
    assert object.coordinates.x == '1.15'
    assert object.token_idempotency == body['token_idempotency']

    type = objects_db.get_types_by_name('человек')
    assert type.type_id == object.type_id
    



