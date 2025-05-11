import asyncio
from scraper.db import init_connection_pool, clear_products, close_pool
from scraper.flipkart_scraper import scrape_flipkart
from scraper.amazon_scraper import scrape_amazon

async def main():
    # Run both scrapers concurrently
    await asyncio.gather(
        scrape_flipkart(),
        scrape_amazon()
    )

if __name__ == "__main__":
    init_connection_pool()

    clear_products()

    # Run the main coroutine
    asyncio.run(main())

    close_pool()