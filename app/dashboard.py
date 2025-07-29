import pandas as pd
import streamlit as st
from datetime import datetime, timedelta

# Load and normalize data
@st.cache_data
def load_data():
    df = pd.read_csv("data/news_tagged_final_combined.csv")

    # Step 1: Parse all dates as timezone-aware (UTC)
    df["published"] = pd.to_datetime(df["published"], errors="coerce", utc=True)

    # Step 2: Drop rows where published is null
    df = df.dropna(subset=["published"])

    # Step 3: Strip timezone info (make datetime naive)
    df["published"] = df["published"].dt.tz_convert(None)

    # Step 4: Fill nulls
    df["risk_tags"] = df["risk_tags"].fillna("")
    df["review_flag"] = df["review_flag"].fillna(False)

    return df

# Load the data
df = load_data()

st.title("📰 Risk News Classifier Dashboard")

# Sidebar filters
vendors = sorted(df["vendor"].dropna().unique())
selected_vendors = st.sidebar.multiselect("Select Vendors", vendors, default=vendors)

# Extract risk tags
tags = sorted({tag.strip() for tags in df["risk_tags"] for tag in str(tags).split(",") if tag.strip()})
selected_tags = st.sidebar.multiselect("Select Risk Tags", tags, default=tags)

# Date filter
days_lookback = st.sidebar.slider("Days Lookback", min_value=1, max_value=30, value=7)
min_date = datetime.utcnow() - timedelta(days=days_lookback)

# Apply filters
filtered_df = df[
    df["vendor"].isin(selected_vendors) &
    (df["published"] >= min_date)
]

if selected_tags:
    filtered_df = filtered_df[
        filtered_df["risk_tags"].apply(lambda x: any(tag in x for tag in selected_tags))
    ]

if st.sidebar.checkbox("Only Show Articles Needing Review"):
    filtered_df = filtered_df[filtered_df["review_flag"] == True]

# Display results
st.markdown(f"### Showing {len(filtered_df)} articles")

for _, row in filtered_df.iterrows():
    st.subheader(row["title"])
    st.write(f"**Vendor:** {row['vendor']} | **Date:** {row['published'].date()} | **Risk Tags:** {row['risk_tags'] or 'None'}")
    st.markdown(f"[🔗 Read full article]({row['url']})")
    if row["review_flag"]:
        st.warning("⚠️ Needs Review: No clear risk tags found")
    st.write("---")

# Export filtered results
st.download_button(
    label="📥 Download Filtered Results as CSV",
    data=filtered_df.to_csv(index=False),
    file_name="filtered_risk_news.csv",
    mime="text/csv"
)
