CREATE TABLE IF NOT EXISTS users (
    id serial PRIMARY KEY,
    name varchar(255) NOT NULL,
    email varchar(255) NOT NULL,
    country_id integer NOT NULL,
    create_dt TIMESTAMP DEFAULT NOW()
);

CREATE TABLE IF NOT EXISTS country (
    id serial PRIMARY KEY,
    name varchar(255) NOT NULL,
    create_dt TIMESTAMP DEFAULT NOW()
);