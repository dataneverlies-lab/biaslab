#!/usr/bin/env python3
import sys
import json
from pathlib import Path
import pandas as pd

# =========================
# CONFIG
# =========================
ABSURD_WORDCOUNT_THRESHOLD = 5000   # >5k słów = podejrzane
VERY_SHORT_THRESHOLD = 5            # <5 słów = ekstremalnie krótkie

# =========================
# ARGS
# =========================
if len(sys.argv) != 2:
    print("Usage: python sanity_check_raw.py <run_id>")
    sys.exit(1)

RUN_ID = sys.argv[1]
RUN_DIR = Path("runs") / RUN_ID
RAW_FILE = RUN_DIR / "raw_responses.jsonl"

if not RAW_FILE.exists():
    raise FileNotFoundError(f"Brak pliku: {RAW_FILE.resolve()}")

# =========================
# LOAD RAW DATA
# =========================
rows = []
with open(RAW_FILE, "r", encoding="utf-8") as f:
    for line in f:
        rows.append(json.loads(line))

df = pd.DataFrame(rows)

print(f"[i] Loaded run: {RUN_ID}")
print(f"[i] Rows: {len(df)}")
print()

# =========================
# BASIC VALIDATION
# =========================
required_cols = {"model", "question_id", "answer"}
missing = required_cols - set(df.columns)
if missing:
    raise RuntimeError(f"Brak wymaganych kolumn: {missing}")

df["word_count"] = df["answer"].astype(str).str.split().str.len()

# =========================
# 1️⃣ WORD COUNT DISTRIBUTION
# =========================
print("=== WORD COUNT DISTRIBUTION (RAW RESPONSES) ===")
wc = df["word_count"]

print(f"min: {wc.min()}")
print(f"max: {wc.max()}")
print(f"mean: {wc.mean():.1f}")
print(f"median: {wc.median():.1f}")

absurd = df[wc > ABSURD_WORDCOUNT_THRESHOLD]
if not absurd.empty:
    print(f"\n[!] ABSURDLY LONG RESPONSES (> {ABSURD_WORDCOUNT_THRESHOLD} words):")
    print(absurd[["model", "question_id", "word_count"]].to_string(index=False))
else:
    print("[✓] No absurdly long responses detected")

very_short = df[wc < VERY_SHORT_THRESHOLD]
if not very_short.empty:
    print(f"\n[!] VERY SHORT RESPONSES (< {VERY_SHORT_THRESHOLD} words):")
    print(very_short[["model", "question_id", "word_count"]].to_string(index=False))
else:
    print("[✓] No extremely short responses detected")

print()

# =========================
# 2️⃣ EMPTY / NULL ANSWERS
# =========================
print("=== EMPTY ANSWER CHECK ===")

empty = df[df["answer"].astype(str).str.strip() == ""]
if not empty.empty:
    print("[!] EMPTY ANSWERS DETECTED:")
    print(empty[["model", "question_id"]].to_string(index=False))
else:
    print("[✓] No empty answers detected")

print()

# =========================
# 3️⃣ PER-MODEL SUMMARY
# =========================
print("=== PER-MODEL SUMMARY ===")

summary = (
    df.groupby("model")
      .agg(
          responses=("answer", "count"),
          avg_words=("word_count", "mean"),
          min_words=("word_count", "min"),
          max_words=("word_count", "max"),
          very_short=("word_count", lambda x: (x < VERY_SHORT_THRESHOLD).sum()),
          absurd_long=("word_count", lambda x: (x > ABSURD_WORDCOUNT_THRESHOLD).sum()),
      )
      .reset_index()
)

print(summary.to_string(index=False))

print()
print("[✓] RAW sanity check completed — no interpretation performed.")
