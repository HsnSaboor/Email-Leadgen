# config.py

# Playwright stealth mode configuration
STEALTH_CONFIG = {
    "headless": True,
    "stealth": True
}

# Output filenames
MAPS_CSV = "maps.csv"
YELLOWPAGES_CSV = "yellowpages.csv"

# User-Agent and other headers
HEADERS = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36",
    "Accept-Language": "en-US,en;q=0.9"
}
