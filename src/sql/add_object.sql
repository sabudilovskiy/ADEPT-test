-- $1: new_object_t
-- $2: created_at
with 
type_v as(
    INSERT INTO objects.types (name) 
    VALUES                    ($1.type_name)
    ON CONFLICT DO NOTHING
    RETURNING type_id
),
inserted as (
    INSERT INTO objects.objects(name, type_id, coordinates, created_at, token)
    SELECT $1.name, type_id, $1.coordinates, $2, $1.token
    FROM type_v
    ON CONFLICT DO NOTHING
    RETURNING object_id, name, $1.type_name, coordinates, created_at
)
SELECT * from inserted;

