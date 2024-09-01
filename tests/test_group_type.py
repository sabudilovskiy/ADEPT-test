from datetime import datetime, timedelta, timezone
import dateutil.parser

import pytest
import uuid

from testsuite.databases import pgsql
from tests.objects_db import Coordinates

K_NOW = datetime(2024, 3, 30, 10, 0, 0, tzinfo=timezone.utc)

@pytest.fixture(name='group_type_db')
def _group_type_db(objects_db):
    class Context:
        def __init__(self, objects_db):
            self.db = objects_db
        
        def add_object(self, name, type_name):
            type_id = self.db.add_type(type_name).type_id
            return self.db.add_object(
                name=name, 
                type_id=type_id,
                coordinates=Coordinates('0', '0'),
                created=K_NOW
            )
    return Context(objects_db)


@pytest.mark.now(K_NOW.isoformat())
async def test_single_type_below_threshold(group_type_db, service_client):
    # Adding objects with one type below the threshold
    group_type_db.add_object('Object 1', 'Type A')
    group_type_db.add_object('Object 2', 'Type A')
    
    N = 3  # Threshold N is greater than the number of objects of 'Type A'
    response = await service_client.get(f'/group/type?N={N}')
    assert response.status == 200
    data = response.json()
    
    groups = {group['type']: group['objects'] for group in data['groups']}
    
    assert 'разное' in groups
    assert len(groups['разное']) == 2
    assert sorted(obj['name'] for obj in groups['разное']) == ['Object 1', 'Object 2']
    assert 'Type A' not in groups

@pytest.mark.now(K_NOW.isoformat())
async def test_multiple_types_below_threshold(group_type_db, service_client):
    # Adding objects with multiple types all below the threshold
    group_type_db.add_object('Object 1', 'Type A')
    group_type_db.add_object('Object 2', 'Type B')
    group_type_db.add_object('Object 3', 'Type C')
    
    N = 2  # Threshold N is greater than the number of objects per type
    response = await service_client.get(f'/group/type?N={N}')
    assert response.status == 200
    data = response.json()
    
    groups = {group['type']: group['objects'] for group in data['groups']}
    
    assert 'разное' in groups
    assert len(groups['разное']) == 3
    assert sorted(obj['name'] for obj in groups['разное']) == ['Object 1', 'Object 2', 'Object 3']
    assert 'Type A' not in groups
    assert 'Type B' not in groups
    assert 'Type C' not in groups

@pytest.mark.now(K_NOW.isoformat())
async def test_one_type_above_threshold(group_type_db, service_client):
    # Adding objects with one type above the threshold
    group_type_db.add_object('Object 1', 'Type A')
    group_type_db.add_object('Object 2', 'Type A')
    group_type_db.add_object('Object 3', 'Type A')
    group_type_db.add_object('Object 4', 'Type B')
    
    N = 2  # Threshold N is less than the number of objects in 'Type A'
    response = await service_client.get(f'/group/type?N={N}')
    assert response.status == 200
    data = response.json()
    
    groups = {group['type']: group['objects'] for group in data['groups']}
    
    assert 'Type A' in groups
    assert len(groups['Type A']) == 3
    assert sorted(obj['name'] for obj in groups['Type A']) == ['Object 1', 'Object 2', 'Object 3']
    
    assert 'разное' in groups
    assert len(groups['разное']) == 1
    assert groups['разное'][0]['name'] == 'Object 4'

@pytest.mark.now(K_NOW.isoformat())
async def test_objects_sorted_within_type(group_type_db, service_client):
    # Adding objects that need to be sorted alphabetically
    group_type_db.add_object('Banana', 'Type A')
    group_type_db.add_object('Apple', 'Type A')
    group_type_db.add_object('Cherry', 'Type A')
    
    N = 2  # Threshold N is less than the number of objects in 'Type A'
    response = await service_client.get(f'/group/type?N={N}')
    assert response.status == 200
    data = response.json()
    
    groups = {group['type']: group['objects'] for group in data['groups']}
    
    assert 'Type A' in groups
    assert len(groups['Type A']) == 3
    assert [obj['name'] for obj in groups['Type A']] == ['Apple', 'Banana', 'Cherry']

@pytest.mark.now(K_NOW.isoformat())
async def test_exact_threshold(group_type_db, service_client):
    # Adding objects with the count exactly equal to the threshold N
    group_type_db.add_object('Object 1', 'Type A')
    group_type_db.add_object('Object 2', 'Type A')
    
    N = 2  # Threshold N is exactly the number of objects in 'Type A'
    response = await service_client.get(f'/group/type?N={N}')
    assert response.status == 200
    data = response.json()
    
    groups = {group['type']: group['objects'] for group in data['groups']}
    
    assert 'разное' in groups
    assert 'Type A' not in groups
    assert len(groups['разное']) == 2
    assert sorted(obj['name'] for obj in groups['разное']) == ['Object 1', 'Object 2']


@pytest.mark.now(K_NOW.isoformat())
async def test_type_named_raznoe(group_type_db, service_client):
    # Adding objects with a type named 'разное'
    group_type_db.add_object('Object 1', 'разное')
    group_type_db.add_object('Object 2', 'Type A')
    
    N = 2  # Threshold N is greater than the number of objects of 'Type A'
    response = await service_client.get(f'/group/type?N={N}')
    assert response.status == 200
    data = response.json()
    
    groups = {group['type']: group['objects'] for group in data['groups']}
    
    # Expect that 'разное' objects stay in their group
    assert 'разное' in groups
    assert len(groups) == 1
    assert groups['разное'][0]['name'] == 'Object 1'
    
    # 'Type A' objects should move to 'разное'
    assert len(groups['разное']) == 2
    assert sorted(obj['name'] for obj in groups['разное']) == ['Object 1', 'Object 2']