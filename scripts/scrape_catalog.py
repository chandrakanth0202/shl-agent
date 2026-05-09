import requests
from bs4 import BeautifulSoup
import json

BASE_URL = "https://www.shl.com/solutions/products/product-catalog/"

response = requests.get(BASE_URL)

soup = BeautifulSoup(response.text, "html.parser")

assessments = []

links = soup.find_all("a")

for link in links:

    name = link.get_text(strip=True)

    href = link.get("href")

    if not href:
        continue

    if "/products/" not in href:
        continue

    full_url = "https://www.shl.com" + href

    assessments.append({

        "name": name,
        "url": full_url,
        "description": name,
        "skills": [],
        "test_type": "Unknown",
        "level": "All"

    })

# remove duplicates
unique = []

seen = set()

for item in assessments:

    if item["url"] not in seen:

        unique.append(item)

        seen.add(item["url"])

with open("app/data/shl_catalog.json", "w") as file:

    json.dump(unique, file, indent=2)

print("Saved", len(unique), "assessments")