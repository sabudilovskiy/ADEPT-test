-- $1: time
SELECT 
    object_id, o.name, t.name, coordinates, created_at
FROM 
    objects.objects o
JOIN 
    objects.types t ON t.type_id = o.type_id
