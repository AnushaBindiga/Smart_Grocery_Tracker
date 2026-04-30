import asyncio
from playwright.async_api import async_playwright
from datetime import date
import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from database import get_connection

async def scrape_carrefour():
    print("Scraping Carrefour promotions...")
    promotions = []

    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=True)
        context = await browser.new_context(
           user_agent="Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
)

        page = await context.new_page()
        
        await page.goto("https://www.carrefour.fr/promotions", 
               wait_until="domcontentloaded", timeout=60000)
        await page.wait_for_timeout(5000)
        
        await page.wait_for_selector(".promotions-product-listing-page", 
                                    timeout=30000)
        
        products = await page.query_selector_all(".product-card-click-wrapper")
        
        for product in products:
            try:
                name = await product.query_selector(".product-card-title")
                price = await product.query_selector(".product-card__price")
                discount = await product.query_selector(".product-card__discount")
                
                name_text = await name.inner_text() if name else "Unknown"
                price_text = await price.inner_text() if price else "0"
                discount_text = await discount.inner_text() if discount else "0%"
                
                promotions.append({
                    "product_name": name_text.strip(),
                    "promo_price": price_text.strip(),
                    "discount": discount_text.strip()
                })
            except:
                continue
        
        await browser.close()
    
    # Save to database
    if promotions:
        conn = get_connection()
        cursor = conn.cursor()
        
        cursor.execute("SELECT id FROM stores WHERE name = 'Carrefour'")
        store = cursor.fetchone()
        
        if store:
            cursor.execute(
                "DELETE FROM promotions WHERE store_id = ?", (store[0],)
            )
            
            for promo in promotions:
                cursor.execute('''
                    INSERT INTO promotions 
                    (store_id, product_name, promo_price, discount, date_scraped)
                    VALUES (?, ?, ?, ?, ?)
                ''', (store[0], promo["product_name"], 
                      promo["promo_price"], promo["discount"],
                      str(date.today())))
            
            conn.commit()
            conn.close()
            print(f"Saved {len(promotions)} Carrefour promotions!")
    else:
        print("No promotions found!")

if __name__ == "__main__":
    asyncio.run(scrape_carrefour())