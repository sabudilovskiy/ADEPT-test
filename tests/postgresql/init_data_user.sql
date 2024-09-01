INSERT INTO todos.users(user_id, login, password)
VALUES('333111c7-9654-4814-b36b-7d39c1ddded2', 'some_login', 'some_password');

INSERT INTO todos.tokens(token_id, user_id, due_ts)
VALUES ('d9ae85b8-6cc5-4e17-a857-a031277113c7',
        '333111c7-9654-4814-b36b-7d39c1ddded2',
        '2024-03-30 06:00:00.000 +0300')
