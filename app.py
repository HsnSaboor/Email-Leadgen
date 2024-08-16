# app.py

import streamlit as st
from google_maps_scraper import scrape_google_maps
from yellowpages_scraper import scrape_yellowpages
from utils import save_to_csv, classify_urls
import config

st.title("Bulk Scraper for Google Maps and Yellow Pages")

# Input textbox for URLs
input_urls = st.text_area("Enter comma-separated URLs:")

if st.button("Start Scraping"):
    urls = [url.strip() for url in input_urls.split(",")]
    
    google_maps_urls, yellowpages_urls = classify_urls(urls)
    
    st.write(f"Found {len(google_maps_urls)} Google Maps URLs.")
    st.write(f"Found {len(yellowpages_urls)} Yellow Pages URLs.")

    # Scrape Google Maps
    if google_maps_urls:
        st.write("Scraping Google Maps...")
        google_maps_results = scrape_google_maps(google_maps_urls)
        save_to_csv(google_maps_results, config.MAPS_CSV)
        st.write(f"Google Maps data saved to {config.MAPS_CSV}")

    # Scrape Yellow Pages
    if yellowpages_urls:
        st.write("Scraping Yellow Pages...")
        yellowpages_results = scrape_yellowpages(yellowpages_urls)
        save_to_csv(yellowpages_results, config.YELLOWPAGES_CSV)
        st.write(f"Yellow Pages data saved to {config.YELLOWPAGES_CSV}")
