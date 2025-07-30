# Risk News Classifier App

This project is a **streamlined risk intelligence tool** that ingests daily news data from multiple sources, classifies it using **zero-shot machine learning**, and tags it with relevant **risk categories** for third-party vendor monitoring. Built with **Streamlit**, **Hugging Face Transformers**, and clean Python pipelines.

## 🔍 Use Case

Supports **Third Party Risk Management** teams who need to:

* Reduce manual hours spent scouring sites like Factiva
* Stay alert to **cybersecurity breaches**, **vendor controversies**, or **negative press**
* Enable internal teams to quickly review and filter flagged vendor news

---

## 🧱 Project Features

### ✅ Data Ingestion

* **GNews API** for recent headlines
* **RSS feeds** for security blogs and alerts
* Vendor-aware & keyword-enriched queries

### 🤖 Risk Tagging

* Uses **zero-shot classification** from Hugging Face to assign risk categories
* Supports multiple tags per article with confidence scoring

### 📊 Interactive Dashboard

* Built with **Streamlit**
* Filter by vendor, risk tag, date, or manual review flag
* Preview full articles and export final datasets to CSV

---

## 📁 Project Structure

```bash
risk-news-classifier/
├── app/
│   └── dashboard.py               # Streamlit app
├── ingestion/
│   ├── news_ingestion.py          # GNews ingestion
│   ├── rss_ingestion.py           # RSS feed ingestion
│   └── merged_news_sources.py     # Merges multiple sources
├── classification/
│   ├── risk_tagger_zero_shot.py   # Zero-shot classifier logic
├── data/
│   ├── vendors.csv                # Vendor list
│   ├── news_articles.csv          # Raw articles from GNews
│   ├── news_articles_rss.csv      # Raw articles from RSS
│   └── news_tagged_final_combined.csv  # Final dataset with tags
├── .env.example              # Template for API keys
├── requirements.txt          # Python dependencies
├── .gitignore                # Hides .env and temp files
└── README.md
```

---

## 🚀 Getting Started

### 1. Clone the Repo

```bash
git clone https://github.com/your-username/risk-news-classifier.git
cd risk-news-classifier
```

### 2. Set Up Environment

```bash
# Create virtual environment
python -m venv venv
source venv/bin/activate  # or venv\Scripts\activate on Windows

# Install dependencies
pip install -r requirements.txt
```

### 3. Set Up API Key

* Copy `.env.example` to `.env`
* Add your [GNews API key](https://gnews.io/docs/) like this:

```
GNEWS_API_KEY=your_api_key_here
```

### 4. Run the App

```bash
streamlit run app/dashboard.py
```

---

## 🧪 Optional: Ingest & Tag Fresh News

Want to pull new data and retag it?

```bash
# Step 1: Pull GNews articles
python ingestion/news_ingestion.py

# Step 2: Pull RSS feed data
python ingestion/rss_ingestion.py

# Step 3: Merge sources
python ingestion/merged_news_sources.py

# Step 4: Tag risk labels using zero-shot classifier
python classification/risk_tagger_zero_shot.py
```

---

## 🤝 Contributions

This is a learning project — contributions, feedback, and ideas are welcome.

---

## 📣 Author

**Ethan Hale**
Senior BI Analyst | M.S. Business Analytics (William & Mary)
Focused on building AI/ML-powered data apps & automation tools.

> Check out my LinkedIn: (https://www.linkedin.com/in/ethan-hale06/)

---

## 📄 License

MIT License (Optional — feel free to include this if you're open to reuse)



# Pipeline Diagram

[news_ingestion.py] ┐
                    ├──> [merged_news_sources.py] ──> news_tagged_final_combined.csv
[rss_ingestion.py] ┘

