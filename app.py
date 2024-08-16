import streamlit as st
from scraper import scrape_google_maps, scrape_yellowpages, scrape_emails_from_websites
import os

st.title("Lead Generation Scraper")
st.write("Scrape phone numbers, websites, emails, and more from Google Maps and Yellow Pages.")

# Sidebar input
category = st.sidebar.text_input("Business Category", value="Yamaha Service Center")
location = st.sidebar.text_input("Location", value="Trivandrum")
number_of_items = st.sidebar.number_input("Number of Items", min_value=1, value=5)
yellowpages_url = st.sidebar.text_input("Yellow Pages URL", value="https://www.yellowpages.com/search?search_terms=service+center&geo_location_terms=Trivandrum")

# Scrape Google Maps
if st.button("Scrape Google Maps"):
    scrape_google_maps(category, location, number_of_items)
    st.success(f"Scraped Google Maps for {category} in {location}. Check the output folder.")

# Scrape Yellow Pages
if st.button("Scrape Yellow Pages"):
    scrape_yellowpages(yellowpages_url)
    st.success(f"Scraped Yellow Pages from {yellowpages_url}. Check the output folder.")

# Scrape Emails from Websites
uploaded_file = st.file_uploader("Upload CSV with Website URLs", type=["csv"])
if uploaded_file and st.button("Scrape Emails"):
    emails = scrape_emails_from_websites(uploaded_file)
    st.json(emails)
    st.success("Scraped emails from websites.")
