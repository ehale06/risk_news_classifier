import feedparser
import pandas as pd
from datetime import datetime
import re

# Define vendors and keywords (same ones used in GNews)
vendors = [
    "Okta", "CrowdStrike", "Cisco", "Microsoft", "Amazon Web Services"
]

risk_keywords = [
    "breach", "hack", "vulnerability", "ransomware", "exploit",
    "leak", "exposure", "cyberattack", "data loss", "compromise"
]

# Define useful RSS feeds
rss_feeds = {
    "TechCrunch Security": "https://techcrunch.com/tag/security/feed/",
    "CyberScoop": "https://www.cyberscoop.com/feed/",
    "The Hacker News": "https://feeds.feedburner.com/TheHackersNews",
    "Dark Reading": "https://www.darkreading.com/rss.xml",
    "Bloomberg Tech": "https://www.bloomberg.com/feeds/podcasts/bloomberg-technology.xml"
}

articles = []

def clean(text):
    return re.sub("<.*?>", "", text or "").strip()

for source, url in rss_feeds.items():
    feed = feedparser.parse(url)
    for entry in feed.entries:
        title = clean(entry.get("title", ""))
        content = clean(entry.get("summary", ""))
        published = entry.get("published", entry.get("updated", None))
        link = entry.get("link", "")

        # Normalize date
        try:
            published_dt = pd.to_datetime(published)
        except:
            published_dt = pd.Timestamp.utcnow()

        combined_text = (title + " " + content).lower()

        for vendor in vendors:
            if vendor.lower() in combined_text:
                if any(keyword in combined_text for keyword in risk_keywords):
                    articles.append({
                        "vendor": vendor,
                        "title": title,
                        "published": published_dt,
                        "url": link,
                        "content": content
                    })
                    break  # Avoid duplicate entries for multiple vendors

# Create DataFrame
df_rss = pd.DataFrame(articles)
df_rss.to_csv("data/news_articles_rss.csv", index=False)
print(f"✅ RSS ingestion complete. {len(df_rss)} articles saved to data/news_articles_rss.csv")
