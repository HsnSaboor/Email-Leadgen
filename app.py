# app.py
import streamlit as st
from google_maps_scraper import scrape_google_maps
from yellowpages_scraper import scrape_yellowpages
from email_scraper import scrape_emails_from_page
from phone_scraper import scrape_phone_numbers_from_page
from address_scraper import scrape_address_from_page
from utils import save_results_to_csv
from config import GOOGLE_MAPS_DOMAIN, YELLOWPAGES_DOMAIN

def process_links(links):
    google_maps_results = []
    yellowpages_results = []

    for i, link in enumerate(links):
        st.progress(i / len(links))

        if GOOGLE_MAPS_DOMAIN in link:
            try:
                data = scrape_google_maps(link)
                data.update({
                    'phone': scrape_phone_numbers_from_page(link),
                    'email': scrape_emails_from_page(link),
                    'address': scrape_address_from_page(link)
                })
                google_maps_results.append(data)
            except Exception as e:
                st.error(f"Failed to process Google Maps link: {link}. Error: {e}")
        elif YELLOWPAGES_DOMAIN in link:
            try:
                data = scrape_yellowpages(link)
                data.update({
                    'phone': scrape_phone_numbers_from_page(link),
                    'email': scrape_emails_from_page(link),
                    'address': scrape_address_from_page(link)
                })
                yellowpages_results.append(data)
            except Exception as e:
                st.error(f"Failed to process Yellow Pages link: {link}. Error: {e}")
        else:
            st.warning(f"Unknown domain in link: {link}")

    return google_maps_results, yellowpages_results

def main():
    st.title("Bulk Lead Generation Scraper")

    input_urls = st.text_area("Enter URLs (comma-separated):", height=200)
    links = [url.strip() for url in input_urls.split(',') if url.strip()]

    if st.button("Start Scraping"):
        st.info("Starting the scraping process...")
        google_maps_results, yellowpages_results = process_links(links)

        if google_maps_results:
            save_results_to_csv(google_maps_results, 'maps.csv')
            st.success("Google Maps data saved to maps.csv")

        if yellowpages_results:
            save_results_to_csv(yellowpages_results, 'yellowpages.csv')
            st.success("Yellow Pages data saved to yellowpages.csv")

if __name__ == "__main__":
    main()
