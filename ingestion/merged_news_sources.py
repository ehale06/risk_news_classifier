import pandas as pd

# Load mock GNews data
gnews_df = pd.read_csv("data/news_articles.csv", parse_dates=["published"])
gnews_df = gnews_df.rename(columns={"description": "description"})  # already named correctly

# Load RSS data
rss_df = pd.read_csv("data/news_articles_rss.csv", parse_dates=["published"])
rss_df = rss_df.rename(columns={"content": "description"})  # normalize to match

# Ensure consistent schema
common_cols = ["vendor", "title", "published", "url", "description"]
gnews_df = gnews_df[common_cols]
rss_df = rss_df[common_cols]

# Combine and deduplicate
combined_df = pd.concat([gnews_df, rss_df], ignore_index=True)
combined_df.drop_duplicates(subset=["title", "url"], inplace=True)

# Save merged file
combined_df.to_csv("data/news_articles_combined.csv", index=False)

print(f"✅ Merged {len(combined_df)} total articles into news_articles_combined.csv")
