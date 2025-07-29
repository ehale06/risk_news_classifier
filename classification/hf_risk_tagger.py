import pandas as pd
from transformers import pipeline

# Load article data
df = pd.read_csv("data/news_articles_combined.csv")  # Change to your file when using real data

# Initialize zero-shot classifier
classifier = pipeline("zero-shot-classification", model="facebook/bart-large-mnli")

# Define risk labels
risk_labels = [
    "Data Breach",
    "Ransomware Attack",
    "Compliance Violation",
    "Lawsuit",
    "Regulatory Fine",
    "System Outage",
    "Malware Attack",
    "DDoS Incident"
]

# Prepare output columns
risk_tags = []
review_flags = []

for _, row in df.iterrows():
    text = row.get("description", "")
    
    if not isinstance(text, str) or text.strip() == "":
        risk_tags.append("")
        review_flags.append(True)
        continue

    result = classifier(text, candidate_labels=risk_labels, multi_label=True)
    
    matched_tags = [label for label, score in zip(result["labels"], result["scores"]) if score >= 0.5]

    risk_tags.append(", ".join(matched_tags))
    review_flags.append(len(matched_tags) == 0)

# Add to dataframe
df["risk_tags"] = risk_tags
df["review_flag"] = review_flags

# Save to file
output_file = "data/news_tagged_final_combined.csv"
df.to_csv(output_file, index=False)

print(f"✅ File saved: {output_file}")
