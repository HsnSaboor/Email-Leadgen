# phone_scraper.py

def extract_phone_numbers(page):
    return page.query_selector(".phone-number").text_content()
