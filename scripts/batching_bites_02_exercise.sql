-- Create sales_reps table
CREATE TABLE sales_reps (
    id SERIAL PRIMARY KEY,
    name VARCHAR(255) NOT NULL,
    region_id INTEGER NOT NULL
);

-- Create regions table
CREATE TABLE regions (
    id SERIAL PRIMARY KEY,
    name VARCHAR(255) NOT NULL
);

-- Create transactions table
CREATE TABLE transactions (
    id SERIAL PRIMARY KEY,
    sales_rep_id INTEGER NOT NULL,
    transaction_date DATE NOT NULL,
    amount NUMERIC(10, 2) NOT NULL
);

-- Insert sample data into regions table
INSERT INTO regions (name) VALUES
    ('North America'),
    ('Europe'),
    ('Asia-Pacific');

-- Insert sample data into sales_reps table
INSERT INTO sales_reps (name, region_id) VALUES
    ('Alice', 1),
    ('Bob', 1),
    ('Charlie', 2),
    ('David', 2),
    ('Eve', 3),
    ('Frank', 3);

-- Insert sample data into transactions table
INSERT INTO transactions (sales_rep_id, transaction_date, amount) VALUES
    (1, '2023-01-01', 1000),
    (1, '2023-01-02', 2000),
    (2, '2023-01-01', 1500),
    (2, '2023-01-03', 1000),
    (3, '2023-01-02', 1700),
    (3, '2023-01-04', 2500),
    (4, '2023-01-03', 800),
    (4, '2023-01-05', 2100),
    (5, '2023-01-04', 1900),
    (5, '2023-01-06', 2200),
    (6, '2023-01-05', 3000),
    (6, '2023-01-07', 1000);
