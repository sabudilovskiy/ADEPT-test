from datetime import datetime, timedelta, timezone
import dateutil.parser

import pytest
import uuid

from testsuite.databases import pgsql
from tests.objects_db import Coordinates

K_NOW = datetime(2024, 3, 30, 10, 0, 0, tzinfo=timezone.utc)

@pytest.fixture(name='group_distance_db')
def _group_distance_db(objects_db):
    class Context:
        def __init__(self, objects_db):
            self.db = objects_db
        
        def add_object(self, name, x, y):
            type_id = self.db.add_type('placeholder').type_id
            return self.db.add_object(
                name=name, 
                type_id=type_id,
                coordinates=Coordinates(x, y),
                created=K_NOW
            )
    return Context(objects_db)


async def test_basic(group_distance_db, service_client):
    # Adding objects within 100 distance
    group_distance_db.add_object('Object 1', x='66', y='33')
    group_distance_db.add_object('Object 2', x='88', y='44')
    
    resp_body = {
        'x': '0',
        'y': '0'
    }
    response = await service_client.post('/group/distance', json=resp_body)
    assert response.status == 200
    data = response.json()
    
    groups = {group['type']: group['items'] for group in data['groups']}
    
    assert 'hundred' in groups
    assert len(groups['hundred']) == 2
    assert sorted(obj['object']['name'] for obj in groups['hundred']) == ['Object 1', 'Object 2']


async def test_thousand_grouping(group_distance_db, service_client):
    # Adding objects within 1000 distance
    group_distance_db.add_object('Object 3', x='500', y='300')
    group_distance_db.add_object('Object 4', x='700', y='400')
    
    resp_body = {
        'x': '0',
        'y': '0'
    }
    response = await service_client.post('/group/distance', json=resp_body)
    assert response.status == 200
    data = response.json()
    
    groups = {group['type']: group['items'] for group in data['groups']}
    
    assert 'thousand' in groups
    assert len(groups['thousand']) == 2
    assert sorted(obj['object']['name'] for obj in groups['thousand']) == ['Object 3', 'Object 4']


async def test_ten_thousand_grouping(group_distance_db, service_client):
    # Adding objects within 10000 distance
    group_distance_db.add_object('Object 5', x='5000', y='6000')
    group_distance_db.add_object('Object 6', x='6000', y='7000')
    
    resp_body = {
        'x': '0',
        'y': '0'
    }
    response = await service_client.post('/group/distance', json=resp_body)
    assert response.status == 200
    data = response.json()
    
    groups = {group['type']: group['items'] for group in data['groups']}
    
    assert 'ten_thousand' in groups
    assert len(groups['ten_thousand']) == 2
    assert sorted(obj['object']['name'] for obj in groups['ten_thousand']) == ['Object 5', 'Object 6']


async def test_far_grouping(group_distance_db, service_client):
    # Adding objects with distance >= 10000
    group_distance_db.add_object('Object 7', x='15000', y='15000')
    group_distance_db.add_object('Object 8', x='20000', y='20000')
    
    resp_body = {
        'x': '0',
        'y': '0'
    }
    response = await service_client.post('/group/distance', json=resp_body)
    assert response.status == 200
    data = response.json()
    
    groups = {group['type']: group['items'] for group in data['groups']}
    
    assert 'far' in groups
    assert len(groups['far']) == 2
    assert sorted(obj['object']['name'] for obj in groups['far']) == ['Object 7', 'Object 8']


async def test_mixed_distances(group_distance_db, service_client):
    # Adding objects across different distance categories
    group_distance_db.add_object('Close Object', x='20', y='20')     # hundred
    group_distance_db.add_object('Near Object', x='600', y='600')    # thousand
    group_distance_db.add_object('Far Object', x='5000', y='5000')   # ten_thousand
    group_distance_db.add_object('Very Far Object', x='15000', y='15000')  # far
    
    resp_body = {
        'x': '0',
        'y': '0'
    }
    response = await service_client.post('/group/distance', json=resp_body)
    assert response.status == 200
    data = response.json()
    
    groups = {group['type']: group['items'] for group in data['groups']}
    
    assert 'hundred' in groups
    assert 'thousand' in groups
    assert 'ten_thousand' in groups
    assert 'far' in groups
    
    assert len(groups['hundred']) == 1
    assert len(groups['thousand']) == 1
    assert len(groups['ten_thousand']) == 1
    assert len(groups['far']) == 1
    
    assert groups['hundred'][0]['object']['name'] == 'Close Object'
    assert groups['thousand'][0]['object']['name'] == 'Near Object'
    assert groups['ten_thousand'][0]['object']['name'] == 'Far Object'
    assert groups['far'][0]['object']['name'] == 'Very Far Object'
