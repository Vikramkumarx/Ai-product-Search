CREATE TABLE IF NOT EXISTS products_vectors (
    product_id INTEGER PRIMARY KEY,
    product_name TEXT,
    category TEXT,
    price REAL,
    rating REAL,
    specifications TEXT,
    vector TEXT
);
