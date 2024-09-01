BEGIN;

CREATE EXTENSION IF NOT EXISTS "uuid-ossp";

CREATE SCHEMA todos;

CREATE TYPE todos.task_status AS ENUM ('completed', 'incomplete');

CREATE TABLE todos.users (
 user_id      UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
 login        TEXT NOT NULL,
 password     TEXT NOT NULL
);

ALTER TABLE todos.users ADD CONSTRAINT unique_login UNIQUE (login);

CREATE TABLE todos.tokens (
  token_id     UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
  user_id      UUID,
  due_ts       TIMESTAMPTZ
);

ALTER TABLE todos.tokens ADD CONSTRAINT fk_user_id FOREIGN KEY (user_id) REFERENCES todos.users(user_id) ON DELETE CASCADE;

CREATE TABLE todos.tasks (
 task_id     UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
 user_id     UUID,
 text        TEXT NOT NULL,
 description TEXT,
 status      todos.task_status NOT NULL,
 due_ts      TIMESTAMPTZ
);

ALTER TABLE todos.tasks ADD CONSTRAINT fk_user_id FOREIGN KEY (user_id) REFERENCES todos.users(user_id) ON DELETE CASCADE;

COMMIT;