# Automated Risk News Classifier
In development — a tool to automate vendor-related risk alerts from news data.


# Pipeline Diagram

[news_ingestion.py] ┐
                    ├──> [merged_news_sources.py] ──> news_tagged_final_combined.csv
[rss_ingestion.py] ┘
