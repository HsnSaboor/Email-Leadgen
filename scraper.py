import requests
from bs4 import BeautifulSoup
from playwright.sync_api import sync_playwright
from shop import Shop
from shop_data import ShopData
import re

def scrape_google_maps(category, location, number_of_items):
    """Scrapes Google Maps for business listings."""
    shop_data_obj = ShopData()
    
    with sync_playwright() as pw:
        browser = pw.chromium.launch(headless=False)
        page = browser.new_page()

        page.goto("https://www.google.com/maps", timeout=10000)
        page.wait_for_timeout(1000)
        page.locator('//input[@id="searchboxinput"]').fill(f"{category} {location}")
        page.wait_for_timeout(1000)
        page.keyboard.press("Enter")
        page.wait_for_timeout(1000)

        page.hover('//a[contains(@href, "https://www.google.com/maps/place")]')
        previously_counted = 0
        
        while True:
            page.mouse.wheel(0, 10000)
            page.wait_for_timeout(3000)

            if page.locator('//a[contains(@href, "https://www.google.com/maps/place")]').count() >= number_of_items:
                listings = page.locator('//a[contains(@href, "https://www.google.com/maps/place")]').all()[:number_of_items]
                print(f"Total Scraped: {len(listings)}")
                break
            else:
                if page.locator('//a[contains(@href, "https://www.google.com/maps/place")]').count() == previously_counted:
                    listings = page.locator('//a[contains(@href, "https://www.google.com/maps/place")]').all()
                    print(f"Arrived at all available\nTotal Scraped: {len(listings)}")
                    break
                else:
                    previously_counted = page.locator('//a[contains(@href, "https://www.google.com/maps/place")]').count()
                    print(f"Currently Scraped: ", previously_counted)

        for listing in listings:
            listing.click()
            page.wait_for_timeout(5000)

            shop_obj = Shop()
            shop_obj.shop_name = listing.get_attribute('aria-label') or ""
            shop_obj.shop_location = page.locator('//button[@data-item-id="address"]//div[contains(@class, "fontBodyMedium")]').first.inner_text() or ""
            shop_obj.website = page.locator('//a[@data-item-id="authority"]//div[contains(@class, "fontBodyMedium")]').first.inner_text() or ""
            shop_obj.contact_number = page.locator('//button[contains(@data-item-id, "phone:tel:")]//div[contains(@class, "fontBodyMedium")]').first.inner_text() or ""
            shop_obj.average_review_count = page.locator('//div[@jsaction="pane.reviewChart.moreReviews"]//span').first.inner_text() or ""
            shop_obj.average_review_points = page.locator('//div[@jsaction="pane.reviewChart.moreReviews"]//div[@role="img"]').first.get_attribute('aria-label') or ""

            shop_data_obj.business_list.append(shop_obj)
        
        shop_data_obj.save_to_csv(f"{category}_in_{location}_google_maps")
        browser.close()

def scrape_yellowpages(yellowpages_url):
    """Scrapes Yellow Pages for business listings."""
    response = requests.get(yellowpages_url)
    soup = BeautifulSoup(response.text, 'html.parser')
    shop_data_obj = ShopData()

    for link_box in soup.select("div.info-section.info-primary"):
        shop_obj = Shop()
        shop_obj.shop_name = link_box.select_one("a.business-name").text.strip()
        shop_obj.shop_location = link_box.select_one("p").text.strip()
        shop_obj.website = link_box.select_one("a.track-visit-website").get('href', '')
        shop_obj.contact_number = link_box.select_one("div.phones.phone.primary").text.strip()

        shop_data_obj.business_list.append(shop_obj)

    shop_data_obj.save_to_csv("yellowpages_scraped")
    
def scrape_emails_from_websites(shop_data_file):
    """Scrapes email addresses from websites of the shops in shop_data_file."""
    df = pd.read_csv(shop_data_file)
    emails = {}

    for index, row in df.iterrows():
        if pd.notna(row['website']):
            response = requests.get(row['website'])
            soup = BeautifulSoup(response.text, 'html.parser')
            email_links = soup.find_all("a", attrs={"href": re.compile("^mailto:")})
            company_name = row['shop_name'] or "Unknown"
            emails[company_name] = [link.get("href").replace("mailto:", "") for link in email_links]

    return emails
