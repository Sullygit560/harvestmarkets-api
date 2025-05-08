# scoring/export_score.py (debug all links)

import requests
from bs4 import BeautifulSoup

def score_export():
    index_url = "https://apps.fas.usda.gov/export-sales/complete.htm"
    page = requests.get(index_url)
    soup = BeautifulSoup(page.text, "html.parser")

    links = soup.find_all("a", href=True)

    print("🔗 All download links found:")
    for link in links:
        href = link["href"]
        if "xls" in href.lower() or "xlsx" in href.lower() or "export" in href.lower():
            print(href)

    return 1  # Placeholder to avoid crashing main.py
