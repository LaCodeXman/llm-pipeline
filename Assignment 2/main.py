import os
import json
import pandas as pd
import logging

from utils.reader import read_txt
from utils.cleaner import clean_text
from utils.chunker import chunk_text
from utils.llm import call_llm
from utils.parser import parse_llm_output

# Setup logging
logging.basicConfig(filename="logs.txt", level=logging.ERROR)

print("🚀 STARTING FULL PIPELINE...")

# File path
current_dir = os.path.dirname(__file__)
file_path = os.path.join(current_dir, "sample.txt")

# Read
text = read_txt(file_path)

# Clean
cleaned = clean_text(text)

# Chunk
chunks = chunk_text(cleaned)

print(f"Total Chunks: {len(chunks)}")

results = []

# -----------------------------
# Helper for sentiment handling
# -----------------------------
def get_sentiment_label(r):
    sentiment = r.get("sentiment")

    if isinstance(sentiment, dict):
        return sentiment.get("label")
    elif isinstance(sentiment, str):
        return sentiment
    return None


# Process each chunk
for i, chunk in enumerate(chunks):
    print(f"\nProcessing chunk {i+1}...")

    try:
        raw_output = call_llm(chunk)

        if not raw_output:
            print("⚠️ Empty response from LLM")
            continue

        print("\nRAW OUTPUT:\n", raw_output)

        parsed = parse_llm_output(raw_output)

        if not parsed:
            print("⚠️ Skipping invalid JSON output")
            continue

        parsed["chunk_id"] = i + 1
        results.append(parsed)

    except Exception as e:
        logging.error(f"Chunk {i+1} failed: {e}")
        print(f"❌ Error in chunk {i+1}: {e}")
        continue


# =========================
# SAVE JSON
# =========================
json_path = os.path.join(current_dir, "outputs.json")

if results:
    with open(json_path, "w") as f:
        json.dump(results, f, indent=2)
    print("✅ JSON saved")
else:
    print("⚠️ No results to save in JSON")


# =========================
# SAVE CSV
# =========================
if results:
    df = pd.json_normalize(results)
    csv_path = os.path.join(current_dir, "outputs.csv")
    df.to_csv(csv_path, index=False)
    print("✅ CSV saved")
else:
    print("⚠️ No data to save in CSV")


# =========================
# GENERATE REPORT
# =========================
positive = sum(1 for r in results if get_sentiment_label(r) == "positive")
neutral = sum(1 for r in results if get_sentiment_label(r) == "neutral")
negative = sum(1 for r in results if get_sentiment_label(r) == "negative")

report = f"""
Report Summary

Total Chunks: {len(results)}

Sentiment:
Positive: {positive}
Neutral: {neutral}
Negative: {negative}
"""

report_path = os.path.join(current_dir, "report.txt")

with open(report_path, "w") as f:
    f.write(report)

print("✅ Report generated")