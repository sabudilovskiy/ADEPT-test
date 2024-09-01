WITH checked_user AS (
    SELECT user_id
    FROM todos.users
    WHERE login = $1 AND password = $2
),
 live_token AS (
     SELECT token_id
     FROM todos.tokens
     WHERE user_id = (SELECT user_id FROM checked_user) AND due_ts >= $3
 ),
 new_token AS (
     INSERT INTO todos.tokens (user_id, due_ts)
         SELECT user_id, $4
         FROM checked_user
         WHERE NOT EXISTS (SELECT 1 FROM live_token)
         RETURNING token_id
 )
SELECT token_id
FROM live_token
UNION ALL
SELECT token_id
FROM new_token;
