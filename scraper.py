import requests
from bs4 import BeautifulSoup
import pandas as pd
from datetime import datetime

URL = "https://www.domain.com.au/sale/melbourne-region-vic/land/"

headers = {
    "User-Agent": "Mozilla/5.0"
}

response = requests.get(URL, headers=headers)
soup = BeautifulSoup(response.text, "html.parser")

listings = []

for prop in soup.find_all("div"):
    try:
        text = prop.get_text(" ", strip=True)

        if len(text) > 50:
            link_tag = prop.find("a", href=True)
            link = ""
            if link_tag:
                link = "https://www.domain.com.au" + link_tag["href"]

            keywords = ["land", "vacant", "development", "subdivision"]
            note = ""

            if any(k in text.lower() for k in keywords):
                note = "TARGET"

            listings.append({
                "Date": datetime.now().strftime("%Y-%m-%d"),
                "Title": text[:120],
                "Price": "",
                "Suburb": "",
                "Land Size": "",
                "Link": link,
                "Notes": note
            })
    except:
        continue

df = pd.DataFrame(listings).drop_duplicates()

df.to_excel("melbourne_property_tracker.xlsx", index=False)

print("✅ Excel file created/updated")