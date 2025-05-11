CREATE TYPE product_type_enum AS ENUM ('mobile', 'laptop', 'tablet');
CREATE TYPE site_enum AS ENUM ('flipkart', 'amazon');

CREATE TABLE product_data (
    id SERIAL PRIMARY KEY,
    site site_enum NOT NULL,
    product_type product_type_enum NOT NULL,
    product_name TEXT NOT NULL,
    product_description TEXT,
    product_image_url TEXT,
    product_price_raw TEXT,
    product_price NUMERIC(10,2),
    product_url TEXT UNIQUE NOT NULL,
    user_rating NUMERIC(3,2),
    ratings_count INTEGER,
    reviews_count INTEGER,
    scraped_at TIMESTAMP DEFAULT NOW()
);

CREATE INDEX idx_product_rating ON product_data(user_rating);
CREATE INDEX idx_product_price ON product_data(product_price);
