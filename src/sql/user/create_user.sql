WITH created_user AS (
    INSERT INTO todos.users (login, password)
    VALUES ($1, $2)
    ON CONFLICT DO NOTHING
    RETURNING user_id
)
 INSERT INTO todos.tokens (user_id, due_ts)
 SELECT user_id, $3
 FROM created_user
 RETURNING token_id;
