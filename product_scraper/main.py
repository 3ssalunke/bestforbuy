import asyncio
from scraper.db import init_connection_pool, clear_products, close_pool
# from scraper.flipkart_scraper import scrape_flipkart
from scraper.amazon_scraper import scrape_amazon

if __name__ == "__main__":
    init_connection_pool()

    clear_products()

    # asyncio.run(scrape_flipkart())
    asyncio.run(scrape_amazon())

    close_pool()