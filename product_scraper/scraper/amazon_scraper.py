from tqdm.asyncio import tqdm
from playwright.async_api import async_playwright
import re
from .db import get_product_types
from .config import AMAZON

async def scrape_amazon():
    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=True)
        page = await browser.new_page()
        page.set_default_timeout(AMAZON["timeout"])

        product_types = get_product_types()

        for product_type in product_types:
            print(f"\n🔍 Starting scrape for product type: {product_type}")

            await page.goto(AMAZON["search_url_template"].format(product_type=product_type, page_number=1))

            pages_to_scrape = AMAZON["max_pages_to_scrape"]

            for page_number in tqdm(range(1, pages_to_scrape + 1), desc=f"Scraping {product_type}", unit="page"):
                await page.goto(AMAZON["search_url_template"].format(product_type=product_type, page_number=page_number))

                products = page.locator(AMAZON["locators"]["product_block"])
                count = await products.count()

                for i in range(count):
                    block = products.nth(i)
                    try:
                        name = await block.locator(AMAZON["locators"]["name"]).inner_text()
                        price_raw = await block.locator(AMAZON["locators"]["price_raw"]).first.inner_text()
                        image_url = await block.locator(AMAZON["locators"]["image_url"]).get_attribute("src")
                        product_url = await block.locator(AMAZON["locators"]["product_url"]).get_attribute("href")
                        full_url = f"{AMAZON['base_url']}{product_url}"

                        rating = ratings_count = reviews_count = None
                        try:
                            rating_element = block.locator(AMAZON["locators"]["rating_element"])
                            await rating_element.hover()
                            await page.wait_for_selector(AMAZON["locators"]["rating_popover"].format(item_number=i+2), timeout=5000)
                            rating_popover_block = page.locator(AMAZON["locators"]["rating_popover"].format(item_number=i+2))

                            rating_text = await rating_popover_block.locator(AMAZON["locators"]["rating_text"]).inner_text()
                            match = re.search(AMAZON["rating_text_regex"], rating_text)
                            if match:
                                rating = float(match.group(1))

                            rating_count_text = await rating_popover_block.locator(AMAZON["locators"]["rating_count_text"]).inner_text()
                            match = re.search(AMAZON["rating_count_text_regex"], rating_count_text)
                            if match:
                                ratings_count = int(match.group(1).replace(",", ""))
                        except Exception as e:
                            print("Exception occured while getting ratings", e)
                            pass
                        
                        print(f"""
                            -------------------------------------------------------------------------------
                            Name: {name}
                            Price Raw: {price_raw}
                            Image URL: {image_url}
                            Product URL: {product_url}
                            Full URL: {full_url}
                            Rating: {rating}
                            Ratings Count: {ratings_count}
                            Reviews Count: {reviews_count}
                            ------------------------------------------------------------------------------""")

                        # product = {
                        #     "site": "flipkart",
                        #     "product_type": product_type,
                        #     "product_name": name,
                        #     "product_description": name,
                        #     "product_image_url": image_url,
                        #     "product_price_raw": price_raw,
                        #     "product_price": float(price_raw.replace("₹", "").replace(",", "").strip()),
                        #     "product_url": full_url,
                        #     "user_rating": float(rating) if rating else None,
                        #     "ratings_count": ratings_count,
                        #     "reviews_count": reviews_count
                        # }

                        # insert_product(product)
                    except Exception as e:
                        print(f"❌ Error on product {i} on page {page_number} ({product_type}): {e}")
                    finally:
                        break

        await browser.close()
