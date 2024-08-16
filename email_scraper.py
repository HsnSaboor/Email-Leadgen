# email_scraper.py
import re
import httpx
from bs4 import BeautifulSoup

def scrape_emails_from_page(url):
    response = httpx.get(url)
    soup = BeautifulSoup(response.text, 'html.parser')
    emails = re.findall(r'[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}', soup.text)
    return emails
