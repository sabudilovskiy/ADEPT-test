BEGIN;

CREATE EXTENSION IF NOT EXISTS "uuid-ossp";

CREATE SCHEMA objects;

CREATE TABLE objects.types (
    type_id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    name TEXT NOT NULL
);

ALTER TABLE objects.types ADD CONSTRAINT types_name_unique UNIQUE (name);
CREATE INDEX idx_name ON objects.types (name);

CREATE TYPE objects.coordinates_t AS (
    x decimal(20, 8), 
    y decimal(20, 8)
);

CREATE TABLE objects.objects (
    object_id   UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    name        TEXT NOT NULL,
    type_id     UUID,
    coordinates objects.coordinates_t NOT NULL,
    created_at  TIMESTAMPTZ,
    token       UUID
);

ALTER TABLE objects.objects ADD CONSTRAINT token_unique UNIQUE (token);
CREATE INDEX idx_token ON objects.objects (token);

ALTER TABLE objects.objects ADD CONSTRAINT type_id_fk FOREIGN KEY (type_id)
REFERENCES objects.types (type_id) MATCH FULL
ON DELETE CASCADE ON UPDATE CASCADE;

CREATE TYPE objects.new_object_t_v1 AS (
    name        TEXT,
    type_name   TEXT,
    coordinates objects.coordinates_t,
    created_at  TIMESTAMPTZ,
    token       UUID
);

CREATE TYPE objects.object_t_v1 AS (
    object_id   UUID,
    name        TEXT,
    type_name   TEXT,
    coordinates objects.coordinates_t,
    created_at  TIMESTAMPTZ
);

CREATE TYPE objects.time_frame_e AS ENUM(
    'later',
    'tomorrow',
    'today',
    'week',
    'month',
    'year',
    'earlier'
);

COMMIT;