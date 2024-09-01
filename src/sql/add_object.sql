-- $1: new_object_t
with 
type_v as (
    INSERT INTO objects.types (name) 
    VALUES ($1.type_name)
    ON CONFLICT (name) DO UPDATE
    SET name = EXCLUDED.name
    RETURNING type_id, name
),
inserted as (
    INSERT INTO objects.objects(name, type_id, coordinates, created_at, token)
    SELECT $1.name, type_id, $1.coordinates, $1.created_at, $1.token
    FROM type_v
    ON CONFLICT(token) DO UPDATE
    SET token = EXCLUDED.token
    RETURNING object_id, name, type_id, coordinates, created_at
)
SELECT object_id, i.name, t.name, coordinates, created_at
FROM inserted i
JOIN type_v t ON i.type_id = t.type_id
