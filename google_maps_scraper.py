# google_maps_scraper.py

from playwright.sync_api import sync_playwright
import config

def scrape_google_maps(urls):
    results = []
    with sync_playwright() as p:
        browser = p.chromium.launch(**config.STEALTH_CONFIG)
        page = browser.new_page()

        for url in urls:
            page.goto(url)
            page.wait_for_timeout(2000)  # wait for 2 seconds

            business_name = page.query_selector("h1").text_content()
            phone_number = page.query_selector(".phone-number").text_content()
            website = page.query_selector(".website").get_attribute("href")
            email = page.query_selector(".email").text_content()
            
            results.append({
                "business_name": business_name,
                "phone_number": phone_number,
                "website": website,
                "email": email,
                "url": url
            })

        browser.close()
    return results
