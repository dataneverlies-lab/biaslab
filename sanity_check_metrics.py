#!/usr/bin/env python3
import sys
import pandas as pd
from pathlib import Path

# =========================
# CONFIG
# =========================
ABSURD_WORDCOUNT_THRESHOLD = 5000   # odpowiedzi > 5k słów traktujemy jako podejrzane
VERY_SHORT_THRESHOLD = 5            # ekstremalnie krótkie odpowiedzi

# =========================
# LOAD DATA
# =========================
if len(sys.argv) != 2:
    print("Usage: python sanity_check_metrics.py <metrics_questions_run_xxx.csv>")
    sys.exit(1)

CSV_PATH = Path(sys.argv[1])

if not CSV_PATH.exists():
    raise FileNotFoundError(f"Brak pliku: {CSV_PATH}")

df = pd.read_csv(CSV_PATH)

print(f"[i] Loaded metrics: {CSV_PATH.name}")
print(f"[i] Rows: {len(df)}")
print()

# =========================
# 1️⃣ WORD COUNT DISTRIBUTION
# =========================
print("=== WORD COUNT DISTRIBUTION ===")

wc = df["word_count"]

print(f"min: {wc.min()}")
print(f"max: {wc.max()}")
print(f"mean: {wc.mean():.1f}")
print(f"median: {wc.median():.1f}")

absurd = df[wc > ABSURD_WORDCOUNT_THRESHOLD]
if not absurd.empty:
    print(f"[!] ABSURDLY LONG RESPONSES (> {ABSURD_WORDCOUNT_THRESHOLD} words):")
    print(absurd[["model", "question_id", "word_count"]].to_string(index=False))
else:
    print("[✓] No absurdly long responses detected")

very_short = df[wc < VERY_SHORT_THRESHOLD]
if not very_short.empty:
    print(f"[!] VERY SHORT RESPONSES (< {VERY_SHORT_THRESHOLD} words):")
    print(very_short[["model", "question_id", "word_count"]].to_string(index=False))
else:
    print("[✓] No extremely short responses detected")

print()

# =========================
# 2️⃣ SPREAD BETWEEN MODELS
# =========================
print("=== INTER-MODEL SPREAD CHECK ===")

spread = df["inter_model_spread_words"]

print(f"spread min: {spread.min()}")
print(f"spread max: {spread.max()}")
print(f"spread mean: {spread.mean():.1f}")
print(f"spread median: {spread.median():.1f}")

low_spread = df[spread == 0]
if not low_spread.empty:
    print("[i] Questions with ZERO spread (identical lengths):")
    print(low_spread[["question_id", "model", "word_count"]].head(10).to_string(index=False))
else:
    print("[✓] No zero-spread anomalies")

print()

# =========================
# 3️⃣ BEHAVIOR COUNTS
# =========================
print("=== BEHAVIOR COUNTS ===")

def count_true(col):
    if col not in df.columns:
        return "N/A"
    return int(df[col].sum())

short_responses = count_true("short_response")
soft_evasions = count_true("soft_evasion")
refusals = count_true("refusal_like")

print(f"Short responses: {short_responses}")
print(f"Soft evasions  : {soft_evasions}")
print(f"Refusals       : {refusals}")

print()

# =========================
# 4️⃣ PER-MODEL SANITY
# =========================
print("=== PER-MODEL SUMMARY ===")

model_stats = (
    df.groupby("model")
      .agg(
          responses=("word_count", "count"),
          avg_words=("word_count", "mean"),
          short_responses=("short_response", "sum") if "short_response" in df else ("word_count", "count"),
          soft_evasions=("soft_evasion", "sum") if "soft_evasion" in df else ("word_count", "count"),
          refusals=("refusal_like", "sum") if "refusal_like" in df else ("word_count", "count"),
      )
      .reset_index()
)

print(model_stats.to_string(index=False))

print()
print("[✓] Sanity check completed — no interpretation performed.")
