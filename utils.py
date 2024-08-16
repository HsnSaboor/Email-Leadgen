# utils.py

import pandas as pd

def save_to_csv(data, filename):
    df = pd.DataFrame(data)
    df.to_csv(filename, index=False)

def classify_urls(urls):
    google_maps_urls = [url for url in urls if "maps.google.com" in url]
    yellowpages_urls = [url for url in urls if "yellowpages.com" in url]
    return google_maps_urls, yellowpages_urls
