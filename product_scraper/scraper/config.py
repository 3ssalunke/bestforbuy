from dotenv import load_dotenv
import os

load_dotenv()

CONNECTION_POOL_CONFIG = {
    "minconn": os.environ.get("POSTGRES_MIN_CONNECTION", 1),
    "maxconn": os.environ.get("POSTGRES_MAX_CONNECTION", 50)
}

DB_CONFIG = {
    "dbname": os.environ.get("POSTGRES_DB"),
    "user": os.environ.get("POSTGRES_USER"),
    "password": os.environ.get("POSTGRES_PASSWORD"),
    "host": os.environ.get("POSTGRES_HOST"),
    "port": int(os.environ.get("POSTGRES_PORT"))
}

FLIPKART = {
    "base_url": "https://www.flipkart.com",
    "search_url_template": "https://www.flipkart.com/search?q={product_type}&page={page_number}",
    "timeout": 10000,
    "max_pages_to_scrape": 5,
    "locators": {
        "pagination": "div._1G0WLw > span",
        "product_block": "div._75nlfW",
        "name": "div.KzDlHZ",
        "price_raw": "div.Nx9bqj._4b5DiR",
        "image_url": "img.DByuf4",
        "product_url": "a.CGtC98",
        "rating": "div.XQDdHH",
        "rating_count_text": "span.Wphh3N",
        "description_item": "ul.G4BRas li.J\\+igdf"
    },
    "pagination_regex": r"Page\s+\d+\s+of\s+(\d+)",
    "ratings_reviews_regex": r"([\d,]+)\s+Ratings.*?([\d,]+)\s+Reviews"
}

AMAZON = {
    "base_url": "https://www.amazon.in",
    "search_url_template": "https://www.amazon.in/s?k={product_type}&page={page_number}",
    "timeout": 10000,
    "max_pages_to_scrape": 5,
    "locators": {
        "product_block": "[role=\"listitem\"] div.s-card-container",
        "name": "h2 span",
        "price_raw": "span.a-price > span.a-offscreen",
        "image_url": "[data-component-type=\"s-product-image\"] img",
        "product_url": "[data-component-type=\"s-product-image\"] a",
        "rating_element": "a.a-popover-trigger",
        "rating_popover": "div#a-popover-{item_number}",
        "rating_text": "h2 span:first-of-type",
        "rating_count_text": "div.a-row"
    },
    "rating_text_regex": r"(\d+(\.\d+)?)\s+out of\s+5",
    "rating_count_text_regex": r"([\d,]+)\s+global ratings"
}
