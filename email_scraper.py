# email_scraper.py

def extract_emails(page):
    return page.query_selector(".email").text_content()
