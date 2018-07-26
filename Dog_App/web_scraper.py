import requests
from bs4 import BeautifulSoup
from google_images_download import google_images_download
from requests.exceptions import HTTPError


# Read in web page for most popular dog breeds
try:
    page = requests.get("https://www.akc.org/expert-advice/news/most-popular-dog-breeds-full-ranking-list/")
except HTTPError:
    print("Page could not be found")
else:
    print("Page downloaded successfully")

soup = BeautifulSoup(page.content, 'html.parser')

# Looked at source code - info found in span style tag
rows = soup.find_all('span', {'style': 'font-weight: 400;'})
dog_breeds = [row.get_text() for row in rows]

# Use google_images_download API to scrape images
response = google_images_download.googleimagesdownload()
for breed in dog_breeds:
    response.download({"keywords": f"{breed} dog",
                       "size": "medium",
                       "limit": 100,
                       "print_urls": True})
