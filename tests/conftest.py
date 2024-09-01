import pathlib
import pytest

from collections import namedtuple
from testsuite.databases.pgsql import discover
from tests.objects_db import ObjectsDbContext

pytest_plugins = ['pytest_userver.plugins.postgresql']

@pytest.fixture(scope='session')
def service_source_dir():
    """Path to root directory service."""
    return pathlib.Path(__file__).parent.parent


@pytest.fixture(scope='session')
def initial_data_path(service_source_dir):
    """Path for find files with data"""
    return [
        service_source_dir / 'tests/postgresql',
        ]

@pytest.fixture(scope='session')
def pgsql_local(service_source_dir, pgsql_local_create):
    """Create schemas databases for tests"""
    databases = discover.find_schemas(
        'pg_service_template',  # service name that goes to the DB connection
        [service_source_dir.joinpath('postgresql')],
    )
    return pgsql_local_create(list(databases.values()))

@pytest.fixture(name='objects_db')
def mock_objects_db(pgsql):
    

    return ObjectsDbContext(pgsql)
