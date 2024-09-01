-- $1: time
SELECT 
    (object_id, o.name, t.name, coordinates, created_at)::objects.object_t_v1 as obj, 
     CASE 
        WHEN created_at::date > ($1::date + INTERVAL '1 day')::date THEN 'later'
        -- Check if created_at is the day after the date part of $1
        WHEN created_at::date = ($1::date + INTERVAL '1 day')::date THEN 'tomorrow'
        -- Check if created_at is the same date as $1
        WHEN created_at::date = $1::date THEN 'today'
        -- Check if created_at is within the same week as $1
        WHEN extract(week from created_at::date) = extract(week from $1::date)
             AND extract(year from created_at::date) = extract(year from $1::date) THEN 'week'
        -- Check if created_at is within the same month as $1
        WHEN extract(month from created_at::date) = extract(month from $1::date)
             AND extract(year from created_at::date) = extract(year from $1::date) THEN 'month'
        -- Check if created_at is within the same year as $1
        WHEN extract(year from created_at::date) = extract(year from $1::date) THEN 'year'
        ELSE 'earlier'
    END as time_frame
FROM 
    objects.objects o
JOIN 
    objects.types t ON t.type_id = o.type_id
ORDER BY
    created_at DESC
