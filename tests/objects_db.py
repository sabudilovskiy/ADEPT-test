from collections import namedtuple
from testsuite.databases.pgsql import discover
import uuid

# SQL query constants
K_GET_ALL_TABLE = """
SELECT * FROM {}
"""

K_GET_OBJECT_BY_ID = """
SELECT * FROM objects.objects WHERE object_id = %s
"""

K_GET_TYPE_BY_NAME = """
SELECT * FROM objects.types WHERE name = %s
"""

K_GET_OBJECTS_BY_TYPE = """
SELECT * FROM objects.objects WHERE type_id = %s
"""

K_INSERT_TYPE = """
INSERT INTO objects.types (type_id, name) VALUES (%s, %s)
RETURNING type_id
"""

K_ADD_TYPE = """
INSERT INTO objects.types (name) VALUES (%s)
ON CONFLICT(name) DO UPDATE SET
name = EXCLUDED.name
RETURNING type_id, name
"""

K_INSERT_OBJECT = """
INSERT INTO objects.objects (object_id, name, type_id, coordinates, created_at, token)
VALUES (%s, %s, %s, %s, %s, %s)
RETURNING object_id
"""

K_ADD_OBJECT = """
INSERT INTO objects.objects (name, type_id, coordinates, created_at, token)
VALUES (%s, %s, %s, %s, %s)
RETURNING object_id, name, type_id, coordinates, created_at, token
"""

class Coordinates(namedtuple('Coordinates', ['x', 'y'])):
    @staticmethod
    def from_db_string(db_string):
        # Remove parentheses and split by comma
        x, y = db_string.strip('()').split(',')
        x = x.rstrip('0').rstrip('.') if '.' in x else x
        y = y.rstrip('0').rstrip('.') if '.' in y else y
        # Return as strings
        return Coordinates(x, y)

class TypeRow(namedtuple('TypeRow', ['type_id', 'name'])):
    pass

class ObjectRow(namedtuple('ObjectRow', ['object_id', 'name', 'type_id', 'coordinates', 'created_at', 'token'])):
    def __new__(cls, object_id, name, type_id, coordinates, created_at, token):
        # Parse the coordinates into a Coordinates namedtuple
        coordinates = Coordinates.from_db_string(coordinates)
        return super().__new__(cls, object_id, name, type_id, coordinates, created_at, token)

class ObjectsDbContext:
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
        cursor.execute(K_GET_OBJECT_BY_ID, (object_id,))
        row = cursor.fetchone()
        return ObjectRow(*row) if row else None

    def get_type_by_name(self, name):
        """Fetch a row from the objects.types table by name and return as TypeRow instance."""
        assert isinstance(name, str)
        cursor = self.db.cursor()
        cursor.execute(K_GET_TYPE_BY_NAME, (name,))
        rows = cursor.fetchall()
        assert len(rows) <= 1
        if len(rows) == 1:
            return TypeRow(*rows[0])
        else:
            return None

    def get_objects_by_type(self, type_id):
        """Fetch rows from the objects.objects table by type_id and return as ObjectRow instances."""
        assert isinstance(type_id, str)
        cursor = self.db.cursor()
        cursor.execute(K_GET_OBJECTS_BY_TYPE, (type_id,))
        rows = cursor.fetchall()
        return [ObjectRow(*row) for row in rows]

    def insert_type(self, type_id, name):
        """Insert a new type into the objects.types table."""
        cursor = self.db.cursor()
        cursor.execute(K_INSERT_TYPE, (type_id, name))
        return cursor.fetchone()[0]  # Return the inserted type_id

    def add_type(self, name):
        """Insert a new type into the objects.types table."""
        cursor = self.db.cursor()
        cursor.execute(K_ADD_TYPE, (name,))
        return TypeRow(*cursor.fetchone())  # Return the inserted type_id

    def insert_object(self, object_id, name, type_id, coordinates, created_at, token):
        """Insert a new object into the objects.objects table."""
        cursor = self.db.cursor()
        coordinates_str = f'({coordinates.x},{coordinates.y})'  # Format coordinates as a string
        cursor.execute(K_INSERT_OBJECT, (object_id, name, type_id, coordinates_str, created_at, token))
        return cursor.fetchone()[0]  # Return the inserted object_id

    def add_object(self, name, type_id, coordinates, created, token=None):
        if token is None:
            token = str(uuid.uuid4())
        cursor = self.db.cursor()
        coordinates_str = f'({coordinates.x},{coordinates.y})'  # Format coordinates as a string
        cursor.execute(K_ADD_OBJECT, (name, type_id, coordinates_str, created, token))
        return ObjectRow(*cursor.fetchone())
        
