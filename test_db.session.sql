
CREATE TABLE Bills (
    id SERIAL PRIMARY KEY,
    date DATE,
    description TEXT,
    money_in NUMERIC,
    money_out NUMERIC,
    balance TEXT,
    category TEXT
);

CREATE TABLE Transport (
    id SERIAL PRIMARY KEY,
    date DATE,
    description TEXT,
    money_in NUMERIC,
    money_out NUMERIC,
    balance TEXT,
    category TEXT
);

CREATE TABLE Groceries (
    id SERIAL PRIMARY KEY,
    date DATE,
    description TEXT,
    money_in NUMERIC,
    money_out NUMERIC,
    balance TEXT,
    category TEXT
);

CREATE TABLE Entertainment (
    id SERIAL PRIMARY KEY,
    date DATE,
    description TEXT,
    money_in NUMERIC,
    money_out NUMERIC,
    balance TEXT,
    category TEXT
);

CREATE TABLE Shopping (
    id SERIAL PRIMARY KEY,
    date DATE,
    description TEXT,
    money_in NUMERIC,
    money_out NUMERIC,
    balance TEXT,
    category TEXT
);

CREATE TABLE Health (
    id SERIAL PRIMARY KEY,
    date DATE,
    description TEXT,
    money_in NUMERIC,
    money_out NUMERIC,
    balance TEXT,
    category TEXT
);

CREATE TABLE Utilities (
    id SERIAL PRIMARY KEY,
    date DATE,
    description TEXT,
    money_in NUMERIC,
    money_out NUMERIC,
    balance TEXT,
    category TEXT
);

CREATE TABLE Other (
    id SERIAL PRIMARY KEY,
    date DATE,
    description TEXT,
    money_in NUMERIC,
    money_out NUMERIC,
    balance TEXT,
    category TEXT
);




