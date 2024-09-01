import pytest
from collections import namedtuple

@pytest.fixture(name='objects_db')
def mock_objects_db(pgsql):
    class Coordinates(namedtuple('Coordinates', ['x', 'y'])):
        pass

    class TypeRow(namedtuple('TypeRow', ['type_id', 'name'])):
        pass

    class ObjectRow(namedtuple('ObjectRow', ['object_id', 'name', 'type_id', 'coordinates', 'created_at', 'token'])):
        def __new__(cls, object_id, name, type_id, coordinates, created_at, token):
            # Parse the coordinates into a Coordinates namedtuple
            coordinates = Coordinates(*coordinates)
            return super().__new__(cls, object_id, name, type_id, coordinates, created_at, token)

    class Context:
        def __init__(self, pgsql):
            self.db = pgsql['objects_db']

        def get_all_from_table(self, table):
            assert isinstance(table, str)
            cursor = self.db.cursor()
            formatted_query = K_GET_ALL_TABLE.format(table)
            cursor.execute(formatted_query)
            return cursor.fetchall()

        def get_types(self):
            """Fetch all rows from the objects.types table and return as TypeRow instances."""
            rows = self.get_all_from_table('objects.types')
            return [TypeRow(*row) for row in rows]

        def get_objects(self):
            """Fetch all rows from the objects.objects table and return as ObjectRow instances."""
            rows = self.get_all_from_table('objects.objects')
            return [ObjectRow(*row) for row in rows]

        def get_object_by_id(self, object_id):
            """Fetch a row from the objects.objects table by object_id and return as ObjectRow instance."""
            assert isinstance(object_id, str)
            cursor = self.db.cursor()
            query = """
            SELECT * FROM objects.objects WHERE object_id = %s
            """
            cursor.execute(query, (object_id,))
            row = cursor.fetchone()
            return ObjectRow(*row) if row else None

        def get_types_by_name(self, name):
            """Fetch rows from the objects.types table by name and return as TypeRow instances."""
            assert isinstance(name, str)
            cursor = self.db.cursor()
            query = """
            SELECT * FROM objects.types WHERE name = %s
            """
            cursor.execute(query, (name,))
            rows = cursor.fetchall()
            return [TypeRow(*row) for row in rows]

        def get_objects_by_type(self, type_id):
            """Fetch rows from the objects.objects table by type_id and return as ObjectRow instances."""
            assert isinstance(type_id, str)
            cursor = self.db.cursor()
            query = """
            SELECT * FROM objects.objects WHERE type_id = %s
            """
            cursor.execute(query, (type_id,))
            rows = cursor.fetchall()
            return [ObjectRow(*row) for row in rows]

    return Context(pgsql)
