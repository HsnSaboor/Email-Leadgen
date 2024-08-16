# phone_scraper.py
import re
import httpx
from bs4 import BeautifulSoup

def scrape_phone_numbers_from_page(url):
    response = httpx.get(url)
    soup = BeautifulSoup(response.text, 'html.parser')
    phones = re.findall(r'\+?\d[\d -]{8,}\d', soup.text)
    return phones
