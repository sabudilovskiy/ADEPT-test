import pathlib

import pytest

from testsuite.databases.pgsql import discover


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


K_GET_ALL_TABLE = """
SELECT * from {}
"""

K_GET_USER_BY_LOGIN = """
SELECT user_id, login, password from todos.users WHERE login = '{}'
"""

K_GET_TOKEN_BY_USER_ID = """
SELECT token_id, user_id, due_ts from todos.tokens WHERE user_id = '{}'
"""


@pytest.fixture(name='todo_db')
def mock_vsu_timetable_db(pgsql):
    class Context:
        def __init__(self, pgsql):
            self.db = pgsql['todo_db']

        def get_all_from_table(self, table):
            assert isinstance(table, str)
            cursor = self.db.cursor()
            formatted_query = K_GET_ALL_TABLE.format(table)
            cursor.execute(formatted_query)
            return cursor.fetchall()

        def get_user_by_login(self, login):
            assert isinstance(login, str)
            cursor = self.db.cursor()
            formatted_query = K_GET_USER_BY_LOGIN.format(login)
            cursor.execute(formatted_query)
            res = cursor.fetchall()
            assert (len(res) == 1)
            return res[0]

        def get_token_by_user_id(self, user_id):
            assert isinstance(user_id, str)
            cursor = self.db.cursor()
            formatted_query = K_GET_TOKEN_BY_USER_ID.format(user_id)
            cursor.execute(formatted_query)
            res = cursor.fetchall()
            assert (len(res) == 1)
            return res[0]

    return Context(pgsql)
