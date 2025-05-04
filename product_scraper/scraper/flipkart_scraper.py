from tqdm.asyncio import tqdm
from playwright.async_api import async_playwright
import re
from .db import get_product_types, insert_product
from .config import FLIPKART

async def scrape_flipkart():
    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=True)
        page = await browser.new_page()
        page.set_default_timeout(FLIPKART["timeout"])

        product_types = get_product_types()

        for product_type in product_types:
            print(f"\n🔍 Starting scrape for product type: {product_type}")

            await page.goto(FLIPKART["search_url_template"].format(product_type=product_type, page_number=1))

            pagination_text = await page.locator(FLIPKART["locators"]["pagination"]).first.inner_text()
            match = re.search(FLIPKART["pagination_regex"], pagination_text)
            total_pages = int(match.group(1)) if match else 1
            pages_to_scrape = min(total_pages, FLIPKART["max_pages_to_scrape"])

            for page_number in tqdm(range(1, pages_to_scrape + 1), desc=f"Scraping {product_type}", unit="page"):
                await page.goto(FLIPKART["search_url_template"].format(product_type=product_type, page_number=page_number))

                products = page.locator(FLIPKART["locators"]["product_block"])
                count = await products.count()

                for i in range(count):
                    block = products.nth(i)
                    try:
                        name = await block.locator(FLIPKART["locators"]["name"]).inner_text()
                        price_raw = await block.locator(FLIPKART["locators"]["price_raw"]).inner_text()
                        image_url = await block.locator(FLIPKART["locators"]["image_url"]).get_attribute("src")
                        product_url = await block.locator(FLIPKART["locators"]["product_url"]).get_attribute("href")
                        full_url = f"{FLIPKART['base_url']}{product_url}"

                        rating = await block.locator(FLIPKART["locators"]["rating"]).inner_text()
                        rating_count_text = await block.locator(FLIPKART["locators"]["rating_count_text"]).inner_text()

                        match = re.search(FLIPKART["ratings_reviews_regex"], rating_count_text)
                        ratings_count = reviews_count = None
                        if match:
                            ratings_count = int(match.group(1).replace(",", ""))
                            reviews_count = int(match.group(2).replace(",", ""))

                        description_items = block.locator(FLIPKART["locators"]["description_item"])
                        li_count = await description_items.count()
                        description_list = [await description_items.nth(j).inner_text() for j in range(li_count)]
                        product_description = ", ".join(map(str.strip, description_list))

                        product = {
                            "site": "flipkart",
                            "product_type": product_type,
                            "product_name": name,
                            "product_description": product_description,
                            "product_image_url": image_url,
                            "product_price_raw": price_raw,
                            "product_price": float(price_raw.replace("₹", "").replace(",", "").strip()),
                            "product_url": full_url,
                            "user_rating": float(rating) if rating else None,
                            "ratings_count": ratings_count,
                            "reviews_count": reviews_count
                        }

                        insert_product(product)
                    except Exception as e:
                        print(f"❌ Error on product {i} on page {page_number} ({product_type}): {e}")

        await browser.close()
