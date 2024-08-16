# address_scraper.py

def extract_addresses(page):
    return page.query_selector(".address").text_content()
