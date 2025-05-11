import psycopg2
import psycopg2.pool
from .config import CONNECTION_POOL_CONFIG, DB_CONFIG

_connection_pool = None

def init_connection_pool():
    global _connection_pool
    if _connection_pool is None:
        _connection_pool = psycopg2.pool.SimpleConnectionPool(
            **CONNECTION_POOL_CONFIG,
            **DB_CONFIG
        )

def get_connection():
    if _connection_pool is None:
        raise Exception("Connection pool is not initialized. Call init_connection_pool() first.")
    return _connection_pool.getconn()

def release_connection(conn):
    if _connection_pool:
        _connection_pool.putconn(conn)

def close_pool():
    if _connection_pool:
        _connection_pool.closeall()

# Database operations below
def clear_products():
    conn = get_connection()
    try:
        with conn.cursor() as cur:
            cur.execute("DELETE FROM product_data;")
        conn.commit()
    finally:
        release_connection(conn)

def get_product_types():
    conn = get_connection()
    try:
        with conn.cursor() as cur:
            cur.execute("SELECT unnest(enum_range(NULL::product_type_enum))")
            return [row[0] for row in cur.fetchall()]
    finally:
        release_connection(conn)

def insert_product(data):
    conn = get_connection()
    try:
        with conn.cursor() as cur:
            cur.execute("""
                INSERT INTO product_data (
                    site, product_type, product_name, product_description,
                    product_image_url, product_price_raw, product_price, product_url, 
                    user_rating, ratings_count, reviews_count
                )
                VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
                ON CONFLICT (product_url) DO NOTHING;
            """, (
                data["site"],
                data["product_type"],
                data["product_name"],
                data.get("product_description"),
                data.get("product_image_url"),
                data.get("product_price_raw"),
                data.get("product_price"),
                data["product_url"],
                data.get("user_rating"),
                data.get("ratings_count"),
                data.get("reviews_count"),
            ))
        conn.commit()
    finally:
        release_connection(conn)
