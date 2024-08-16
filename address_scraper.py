# address_scraper.py
import httpx
from bs4 import BeautifulSoup

def scrape_address_from_page(url):
    response = httpx.get(url)
    soup = BeautifulSoup(response.text, 'html.parser')
    address = soup.find("address")
    return address.text.strip() if address else "N/A"
