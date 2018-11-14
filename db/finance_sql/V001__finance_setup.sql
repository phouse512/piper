-- create table for basic finance analysis

CREATE TABLE budgets (
    id SERIAL NOT NULL PRIMARY KEY,
    home_id INT,
    name VARCHAR NOT NULL,
    created_at BIGINT NOT NULL DEFAULT (EXTRACT(epoch FROM NOW()) * 1000)
);

CREATE TABLE accounts (
    id SERIAL NOT NULL PRIMARY KEY,
    budget_id INT NOT NULL REFERENCES budgets (id),
    name VARCHAR NOT NULL,
    parent_id INT REFERENCES accounts (id),
    created_at BIGINT NOT NULL DEFAULT (EXTRACT(epoch FROM NOW()) * 1000)
);

CREATE TABLE record_source (
    id SERIAL NOT NULL PRIMARY KEY,
    budget_id INT NOT NULL REFERENCES budgets (id),
    source_key VARCHAR NOT NULL,
    source_type VARCHAR NOT NULL,
    record_count INT NOT NULL,
    created_at BIGINT NOT NULL DEFAULT (EXTRACT(epoch FROM NOW()) * 1000)
);

CREATE TABLE records (
    id SERIAL NOT NULL PRIMARY KEY,
    hash VARCHAR NOT NULL,
    budget_id INT NOT NULL REFERENCES budgets (id),
    from_account_id INT REFERENCES accounts (id),
    to_account_id INT REFERENCES accounts (id),
    amount INT NOT NULL,
    description VARCHAR NOT NULL,
    transaction_time INT NOT NULL,
    record_source_id INT NOT NULL REFERENCES record_source (id),
    created_at BIGINT NOT NULL DEFAULT (EXTRACT(epoch FROM NOW()) * 1000)
);
