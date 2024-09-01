from datetime import datetime

import pytest

from testsuite.databases import pgsql
from tests.objects_db import Coordinates


async def test_ok(service_client, objects_db):
    body = {
        "name": "Игорь",
        "coordinates": {
            "x": "0.132",
            "y": "1.15"
        },
        "type_name": "человек",
        "token_idempotency": "e7df97a2-278d-476a-98ca-3f31ef6cf5c8",
        "created_at": '2024-03-29T23:00:00+00:00'
    }
    response = await service_client.post(
        '/object',
        json=body,
    )
    assert response.status == 200
    object_id = response.json()['object_id']
    object = objects_db.get_object_by_id(object_id)
    assert object.name == 'Игорь'
    assert object.coordinates.x == '0.132'
    assert object.coordinates.y == '1.15'
    assert object.created_at == datetime.fromisoformat('2024-03-29T23:00:00+00:00')
    assert object.token == body['token_idempotency']

    type = objects_db.get_type_by_name('человек')
    assert type.type_id == object.type_id
    

async def test_idempotency(service_client, objects_db):
    body = {
        "name": "Игорь",
        "coordinates": {
            "x": "0.132",
            "y": "1.15"
        },
        "type_name": "человек",
        "token_idempotency": "e7df97a2-278d-476a-98ca-3f31ef6cf5c8",
        "created_at": '2024-03-31T05:00:00.000+0300'
    }
    response = await service_client.post(
        '/object',
        json=body,
    )
    assert response.status == 200
    object_id = response.json()['object_id']
    object = objects_db.get_object_by_id(object_id)
    assert object.name == 'Игорь'
    assert object.coordinates.x == '0.132'
    assert object.coordinates.y == '1.15'
    assert object.created_at == datetime.fromisoformat('2024-03-29T23:00:00+00:00')
    assert object.token == body['token_idempotency']

    type = objects_db.get_type_by_name('человек')
    assert type.type_id == object.type_id
    

async def test_idempotency(service_client, objects_db):
    # Step 1: Add a type to the database
    type_id = objects_db.insert_type('f27aecc3-5040-459e-b868-0f0701a3fb05', 'человек')
    
    # Step 2: Manually add an object with a specific created_at time
    existing_object_id = 'e7df97a2-278d-476a-98ca-3f31ef6cf5c8'
    created_at = '2024-03-29T23:00:00+00:00'
    coordinates = Coordinates('0.132', '1.15')
    token = 'e7df97a2-278d-476a-98ca-3f31ef6cf5c8'
    
    objects_db.insert_object(
        object_id=existing_object_id,
        name='Игорь',
        type_id=type_id,
        coordinates=coordinates,
        created_at=created_at,
        token=token
    )
    
    # Step 3: Call the endpoint with the same token_idempotency
    body = {
        "name": "Игорь",
        "coordinates": {
            "x": "0.132",
            "y": "1.15"
        },
        "type_name": "человек",
        "token_idempotency": token,
        "created_at": '2024-03-31T05:00:00.000+0300'
    }
    
    response = await service_client.post(
        '/object',
        json=body,
    )
    
    # Step 4: Assert that the response is OK and contains the correct object_id
    assert response.status == 200
    response_object_id = response.json()['object_id']
    assert response_object_id == existing_object_id
    
    # Step 5: Fetch the object from the database again
    object = objects_db.get_object_by_id(response_object_id)
    
    # Step 6: Assert that the object's fields match the expected values and have not changed
    assert object.name == 'Игорь'
    assert object.coordinates.x == '0.132'
    assert object.coordinates.y == '1.15'
    assert object.created_at == datetime.fromisoformat(created_at)
    assert object.token == token
    
    # Step 7: Ensure the type is correctly associated
    type_in_db = objects_db.get_type_by_name('человек')
    assert type_in_db.type_id == object.type_id

    # Step 8: Ensure that the number of objects in the database did not change (indicating no new object was added)
    objects_with_same_token = objects_db.get_objects_by_type(type_id)
    assert len(objects_with_same_token) == 1