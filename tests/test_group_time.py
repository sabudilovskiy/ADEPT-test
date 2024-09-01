from datetime import datetime, timedelta, timezone
import dateutil.parser

import pytest
import uuid

from testsuite.databases import pgsql
from tests.objects_db import Coordinates

K_NOW = datetime(2024, 3, 30, 10, 0, 0, tzinfo=timezone.utc)

@pytest.fixture(name='group_time_db')
def _group_time_db(objects_db):
    class Context:
        def __init__(self, objects_db):
            self.db = objects_db
        
        def add_object(self, name, type_name, created):
            type_id = self.db.add_type(type_name).type_id
            return self.db.add_object(
                name=name, 
                type_id=type_id,
                coordinates=Coordinates('0', '0'),
                created=created
            )

        def add_object_later(self, name, type_name):
            return self.add_object(
                name=name, 
                type_name=type_name,
                created=K_NOW + timedelta(days=3)
            )
        
        def add_object_tomorrow(self, name, type_name):
            return self.add_object(
                name=name, 
                type_name=type_name,
                created=K_NOW + timedelta(days=1)
            )
        
        def add_object_today(self, name, type_name):
            return self.add_object(
                name=name, 
                type_name=type_name,
                created=K_NOW + timedelta(hours=1)
            )
        def add_object_weekly(self, name, type_name):
            return self.add_object(
                name=name, 
                type_name=type_name,
                created=K_NOW - timedelta(days=5)
            )
        
        def add_object_mounthly(self, name, type_name):
            return self.add_object(
                name=name, 
                type_name=type_name,
                created=K_NOW - timedelta(days=25)
            )
        def add_object_yearly(self, name, type_name):
            return self.add_object(
                name=name, 
                type_name=type_name,
                created=K_NOW - timedelta(days=40)
            )
        def add_object_earlier(self, name, type_name):
            return self.add_object(
                name=name, 
                type_name=type_name,
                created=K_NOW - timedelta(days=365)
            )
    return Context(objects_db)

@pytest.mark.now(K_NOW.isoformat())
async def test_objects_earlier(group_time_db, service_client):
    group_time_db.add_object_earlier('Earliest Object', 'Type A')
    
    response = await service_client.get('/group/time')
    assert response.status == 200
    data = response.json()
    
    frames = {frame['type']: frame['objects'] for frame in data['frames']}
    
    assert len(frames['earlier']) == 1
    assert frames['earlier'][0]['name'] == 'Earliest Object'

@pytest.mark.now(K_NOW.isoformat())
async def test_objects_yearly(group_time_db, service_client):
    group_time_db.add_object_yearly('Yearly Object', 'Type B')
    
    response = await service_client.get('/group/time')
    assert response.status == 200
    data = response.json()
    
    frames = {frame['type']: frame['objects'] for frame in data['frames']}
    
    assert len(frames['year']) == 1
    assert frames['year'][0]['name'] == 'Yearly Object'

@pytest.mark.now(K_NOW.isoformat())
async def test_objects_monthly(group_time_db, service_client):
    group_time_db.add_object_mounthly('Monthly Object', 'Type C')
    
    response = await service_client.get('/group/time')
    assert response.status == 200
    data = response.json()
    
    frames = {frame['type']: frame['objects'] for frame in data['frames']}
    
    assert len(frames['month']) == 1
    assert frames['month'][0]['name'] == 'Monthly Object'

@pytest.mark.now(K_NOW.isoformat())
async def test_objects_weekly(group_time_db, service_client):
    group_time_db.add_object_weekly('Weekly Object', 'Type D')
    
    response = await service_client.get('/group/time')
    assert response.status == 200
    data = response.json()
    
    frames = {frame['type']: frame['objects'] for frame in data['frames']}
    
    assert len(frames['week']) == 1
    assert frames['week'][0]['name'] == 'Weekly Object'

@pytest.mark.now(K_NOW.isoformat())
async def test_objects_today(group_time_db, service_client):
    group_time_db.add_object_today('Today Object', 'Type E')
    
    response = await service_client.get('/group/time')
    assert response.status == 200
    data = response.json()
    
    frames = {frame['type']: frame['objects'] for frame in data['frames']}
    
    assert len(frames['today']) == 1
    assert frames['today'][0]['name'] == 'Today Object'


@pytest.mark.now(K_NOW.isoformat())
async def test_objects_tomorrow(group_time_db, service_client):
    group_time_db.add_object_tomorrow('Tomorrow Object', 'Type F')
    
    response = await service_client.get('/group/time')
    assert response.status == 200
    data = response.json()
    
    frames = {frame['type']: frame['objects'] for frame in data['frames']}
    
    assert len(frames['tomorrow']) == 1
    assert frames['tomorrow'][0]['name'] == 'Tomorrow Object'

@pytest.mark.now(K_NOW.isoformat())
async def test_objects_later(group_time_db, service_client):
    group_time_db.add_object_later('Later Object', 'Type F')
    
    response = await service_client.get('/group/time')
    assert response.status == 200
    data = response.json()
    
    frames = {frame['type']: frame['objects'] for frame in data['frames']}
    
    assert len(frames['later']) == 1
    assert frames['later'][0]['name'] == 'Later Object'


@pytest.mark.now(K_NOW.isoformat())
async def test_objects_sorted_by_creation_time(group_time_db, service_client):
    names = ['Object 1', 'Object 2', 'Object 3', 'Object 4', 'Object 5']
    
    # Add multiple objects with varying timestamps to the 'today' time frame
    timestamps = [
        K_NOW - timedelta(hours=7),
        K_NOW - timedelta(hours=6),
        K_NOW - timedelta(hours=3),
        K_NOW - timedelta(hours=1),
        K_NOW
    ]
    
    for name, timestamp in zip(names, timestamps):
        object = group_time_db.add_object(name=name, type_name='Type G', created=timestamp.isoformat())
    
    # Fetch the objects from the '/group/time' endpoint
    response = await service_client.get('/group/time')
    assert response.status == 200
    data = response.json()
    
    # Extract objects from the 'today' frame
    frames = {frame['type']: frame['objects'] for frame in data['frames']}
    today_objects = frames['today']
    
    # Convert the 'created_at' timestamps in the response to datetime objects in UTC
    def parse_created_at(obj):
        dt = dateutil.parser.isoparse(obj['created_at'])
        if dt.tzinfo is None:
            dt = dt.replace(tzinfo=timezone.utc)  # Assume naive dates are in UTC
        return dt.astimezone(timezone.utc)
    
    today_objects_sorted = sorted(today_objects, key=parse_created_at, reverse=True)
    
    # Assert that the objects are sorted by 'created_at' in descending order
    assert today_objects == today_objects_sorted
    
    # Additionally, assert that the sorted order matches the input timestamps
    expected_order = sorted(timestamps, reverse=True)
    actual_order = [parse_created_at(obj) for obj in today_objects]
    
    assert [dt.isoformat() for dt in actual_order] == [dt.isoformat() for dt in expected_order]
