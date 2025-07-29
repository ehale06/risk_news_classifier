import pandas as pd
import requests
import time
import os
from datetime import datetime, timedelta
from dotenv import load_dotenv
from textwrap import wrap

load_dotenv()
GNEWS_API_KEY = os.getenv("GNEWS_API_KEY")

# Load vendors
vendors_df = pd.read_csv("data/vendors.csv")
vendors = vendors_df["vendor"].dropna().tolist()

# Define keywords (tunable)
keywords = [
    "data breach", "ransomware", "cyber attack", "security incident",
    "regulatory fine", "lawsuit", "compliance failure", "system outage",
    "DDoS attack", "hacking", "fraud", "whistleblower", "misconduct"
]

# Config
DAYS_BACK = 1
KEYWORDS_PER_BATCH = 3  # Tune based on average length to stay < 200 chars
MAX_ARTICLES_PER_QUERY = 10
API_SLEEP_SECONDS = 4
BASE_URL = "https://gnews.io/api/v4/search"

# Function to create keyword batches
def chunk_keywords(keyword_list, size):
    for i in range(0, len(keyword_list), size):
        yield keyword_list[i:i + size]

# Track articles
all_articles = []

# Loop through days and vendors
for day_offset in range(DAYS_BACK):
    date = datetime.now() - timedelta(days=day_offset)
    from_date = date.strftime("%Y-%m-%d")
    to_date = from_date

    for vendor in vendors:
        for kw_batch in chunk_keywords(keywords, KEYWORDS_PER_BATCH):
            keyword_query = " OR ".join([f'"{kw}"' for kw in kw_batch])
            query = f'"{vendor}" AND ({keyword_query})'

            if len(query) > 200:
                print(f"⚠️ Skipped query due to length: {query}")
                continue

            print(f"🔎 Fetching: {query} on {from_date}")

            params = {
                "q": query,
                "from": from_date,
                "to": to_date,
                "lang": "en",
                "sort_by": "relevance",
                "max": MAX_ARTICLES_PER_QUERY,
                "token": GNEWS_API_KEY
            }

            try:
                response = requests.get(BASE_URL, params=params)
                time.sleep(API_SLEEP_SECONDS)

                if response.status_code != 200:
                    print(f"❌ Error {response.status_code}: {response.text}")
                    continue

                data = response.json()
                articles = data.get("articles", [])

                for article in articles:
                    all_articles.append({
                        "vendor": vendor,
                        "title": article["title"],
                        "description": article["description"],
                        "content": article.get("content", ""),
                        "url": article["url"],
                        "published": article["publishedAt"]
                    })

            except Exception as e:
                print(f"🚨 Exception: {e}")
                continue

# Deduplicate and save
df = pd.DataFrame(all_articles)
df.drop_duplicates(subset="url", inplace=True)
df.to_csv("data/news_articles.csv", index=False)
print(f"✅ Saved {len(df)} unique articles to news_articles.csv")
