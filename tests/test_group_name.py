from datetime import datetime, timedelta, timezone
import dateutil.parser

import pytest
import uuid

from testsuite.databases import pgsql
from tests.objects_db import Coordinates

K_NOW = datetime(2024, 3, 30, 10, 0, 0, tzinfo=timezone.utc)

@pytest.fixture(name='group_name_db')
def _group_name_db(objects_db):
    class Context:
        def __init__(self, objects_db):
            self.db = objects_db
        
        def add_object(self, name):
            type_id = self.db.add_type('placeholder').type_id
            return self.db.add_object(
                name=name, 
                type_id=type_id,
                coordinates=Coordinates('0', '0'),
                created=K_NOW
            )
    return Context(objects_db)


async def test_basic(group_name_db, service_client):
    # Adding objects with non-Cyrillic characters
    group_name_db.add_object('Object 2')
    group_name_db.add_object('Object 1')
    
    response = await service_client.get('/group/name')
    assert response.status == 200
    data = response.json()
    
    groups = {group['first_letter']: group['objects'] for group in data['groups']}
    
    assert '#' in groups
    assert len(groups['#']) == 2
    assert sorted(obj['name'] for obj in groups['#']) == ['Object 1', 'Object 2']


async def test_cyrillic_grouping(group_name_db, service_client):
    # Adding objects with Cyrillic names
    group_name_db.add_object('Яблоко')
    group_name_db.add_object('Банан')
    group_name_db.add_object('Арбуз')
    
    response = await service_client.get('/group/name')
    assert response.status == 200
    data = response.json()
    
    groups = {group['first_letter']: group['objects'] for group in data['groups']}
    
    assert 'А' in groups
    assert 'Б' in groups
    assert 'Я' in groups
    
    assert len(groups['А']) == 1
    assert len(groups['Б']) == 1
    assert len(groups['Я']) == 1
    
    assert groups['А'][0]['name'] == 'Арбуз'
    assert groups['Б'][0]['name'] == 'Банан'
    assert groups['Я'][0]['name'] == 'Яблоко'


async def test_mixed_characters(group_name_db, service_client):
    # Adding objects with a mix of Cyrillic and non-Cyrillic names
    group_name_db.add_object('Яблоко')
    group_name_db.add_object('Apple')
    group_name_db.add_object('Арбуз')
    group_name_db.add_object('Banana')
    
    response = await service_client.get('/group/name')
    assert response.status == 200
    data = response.json()
    
    groups = {group['first_letter']: group['objects'] for group in data['groups']}
    
    assert 'А' in groups
    assert 'Я' in groups
    assert '#' in groups
    
    assert len(groups['А']) == 1
    assert len(groups['Я']) == 1
    assert len(groups['#']) == 2
    
    assert groups['А'][0]['name'] == 'Арбуз'
    assert groups['Я'][0]['name'] == 'Яблоко'
    assert sorted(obj['name'] for obj in groups['#']) == ['Apple', 'Banana']


async def test_non_cyrillic_grouping(group_name_db, service_client):
    # Adding objects with non-Cyrillic characters
    group_name_db.add_object('Zebra')
    group_name_db.add_object('Xylophone')
    group_name_db.add_object('1234')
    group_name_db.add_object('!!!')
    
    response = await service_client.get('/group/name')
    assert response.status == 200
    data = response.json()
    
    groups = {group['first_letter']: group['objects'] for group in data['groups']}
    
    assert '#' in groups
    assert len(groups['#']) == 4
    assert sorted(obj['name'] for obj in groups['#']) == ['!!!', '1234', 'Xylophone', 'Zebra']


async def test_mixed_cyrillic_non_cyrillic(group_name_db, service_client):
    # Adding objects with Cyrillic and non-Cyrillic first letters
    group_name_db.add_object('Кот')
    group_name_db.add_object('Кошка')
    group_name_db.add_object('Dog')
    group_name_db.add_object('Дельфин')
    
    response = await service_client.get('/group/name')
    assert response.status == 200
    data = response.json()
    
    groups = {group['first_letter']: group['objects'] for group in data['groups']}
    
    assert 'К' in groups
    assert 'Д' in groups
    assert '#' in groups
    
    assert len(groups['К']) == 2
    assert len(groups['Д']) == 1
    assert len(groups['#']) == 1
    
    assert sorted(obj['name'] for obj in groups['К']) == ['Кот', 'Кошка']
    assert groups['Д'][0]['name'] == 'Дельфин'
    assert groups['#'][0]['name'] == 'Dog'
