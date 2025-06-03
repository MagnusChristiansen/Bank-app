-- sql_ddl/schema.sql

CREATE TABLE users (
    id      SERIAL PRIMARY KEY,
    name    VARCHAR(50) NOT NULL,
    balance NUMERIC      NOT NULL DEFAULT 0
);

CREATE TABLE transactions (
    id         SERIAL PRIMARY KEY,
    user_id    INTEGER   NOT NULL REFERENCES users(id),
    amount     NUMERIC   NOT NULL,
    type       VARCHAR(20) NOT NULL,
    timestamp  TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP
);

