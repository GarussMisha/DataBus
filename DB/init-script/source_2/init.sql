CREATE TABLE IF NOT EXISTS country (
    id serial PRIMARY KEY,
    name varchar(255) NOT NULL,
    create_dt TIMESTAMP DEFAULT NOW()
)