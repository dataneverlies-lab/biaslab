#!/usr/bin/env python3
import sys
import json
import pandas as pd
from pathlib import Path
from collections import Counter

# =========================
# CONFIG
# =========================
WEIGHTS = {
    "spread": 0.55,
    "gap": 0.30,
    "short": 0.15,
}

TOP_K = 5

BASE_DIR = Path(__file__).resolve().parent
REPORTS_DIR = BASE_DIR / "reports"

# =========================
# ARGUMENTS
# =========================
if len(sys.argv) != 2:
    print("Usage: python top5_insights.py <run_id>")
    sys.exit(1)

RUN_ID = sys.argv[1]

METRICS_CSV = REPORTS_DIR / f"metrics_questions_run_{RUN_ID}.csv"
QUESTIONS_JSON = REPORTS_DIR / f"raport_questions_run_{RUN_ID}.json"

if not METRICS_CSV.exists():
    raise FileNotFoundError(f"Missing metrics CSV: {METRICS_CSV.resolve()}")

if not QUESTIONS_JSON.exists():
    raise FileNotFoundError(f"Missing report JSON: {QUESTIONS_JSON.resolve()}")

OUT_JSON = REPORTS_DIR / f"top5_insights_{RUN_ID}.json"
OUT_MD = REPORTS_DIR / f"top5_insights_{RUN_ID}.md"

# =========================
# LOAD DATA
# =========================
df = pd.read_csv(METRICS_CSV)

with open(QUESTIONS_JSON, encoding="utf-8") as f:
    report = json.load(f)

questions = report["questions"]

# =========================
# NORMALIZATION
# =========================
def minmax(series):
    if series.max() == series.min():
        return series * 0
    return (series - series.min()) / (series.max() - series.min())

df["n_spread"] = minmax(df["spread_words"])
df["n_gap"] = minmax(df["gap_ratio"])
df["n_short"] = minmax(df["short_responses"])

df["score"] = (
    WEIGHTS["spread"] * df["n_spread"]
    + WEIGHTS["gap"] * df["n_gap"]
    + WEIGHTS["short"] * df["n_short"]
)

top = df.sort_values("score", ascending=False).head(TOP_K)

# =========================
# TITLE GENERATOR (CLEAN, SCIENTIFIC)
# =========================
def generate_title(row):
    if row["short_responses"] > 0:
        return "Asymetria narracyjna w odpowiedziach normatywnych modeli"
    if row["gap_ratio"] > 10:
        return "Znaczna rozbieżność długości narracji między modelami"
    return "Różnice strategii narracyjnych modeli językowych"

# =========================
# META-INSIGHT
# =========================
sections = []
for qid in top["question_id"]:
    q = questions.get(qid)
    if q:
        sections.append(q.get("section"))

section_counts = Counter(sections)

meta_insight = (
    "Wszystkie pytania z Top-5 dotyczą normatywnych reakcji platform cyfrowych. "
    "Sugeruje to, że ten typ pytań najczęściej ujawnia różnice w domyślnych "
    "strategiach narracyjnych modeli językowych."
)

# =========================
# BUILD OUTPUT
# =========================
insights_out = []

for _, row in top.iterrows():
    qid = row["question_id"]
    q = questions[qid]

    responses = q["responses"]
    words = {m: r["words"] for m, r in responses.items()}

    shortest = min(words, key=words.get)
    longest = max(words, key=words.get)

    insights_out.append({
        "question_id": qid,
        "section": q["section"],
        "prompt": q["prompt"],
        "spread_words": int(row["spread_words"]),
        "gap_ratio": float(row["gap_ratio"]),
        "short_responses": int(row["short_responses"]),
        "shortest_model": shortest,
        "longest_model": longest,
        "title": generate_title(row),
        "insight": (
            f"Pytanie ujawnia {int(row['spread_words'])} słów różnicy długości odpowiedzi "
            f"(relacja max/min {row['gap_ratio']:.2f}×). "
            f"Najkrócej odpowiada {shortest}, a najbardziej rozwija temat {longest}. "
            f"Obecność krótkiej odpowiedzi sugeruje ostrożność lub ograniczenie narracji."
        ),
        "why_it_matters": (
            "Wskazuje to na odmienne domyślne strategie narracyjne modeli "
            "w odpowiedziach normatywnych."
        )
    })

# =========================
# SAVE JSON
# =========================
with open(OUT_JSON, "w", encoding="utf-8") as f:
    json.dump({
        "run_id": RUN_ID,
        "meta_insight": meta_insight,
        "top5": insights_out
    }, f, indent=2, ensure_ascii=False)

# =========================
# SAVE MARKDOWN
# =========================
with open(OUT_MD, "w", encoding="utf-8") as f:
    f.write("# BiasLab — Top 5 insights (rule-based)\n\n")
    f.write(f"**Run:** `{RUN_ID}`\n\n")
    f.write("## Meta-insight\n\n")
    f.write(meta_insight + "\n\n---\n\n")

    for i, ins in enumerate(insights_out, 1):
        f.write(f"## {i}. {ins['title']}\n\n")
        f.write(f"**ID:** `{ins['question_id']}`  \n")
        f.write(f"**Sekcja:** `{ins['section']}`\n\n")
        f.write(f"**Pytanie:** {ins['prompt']}\n\n")
        f.write(
            f"**Metryki:** spread={ins['spread_words']} słów · "
            f"gap={ins['gap_ratio']:.2f}× · short={ins['short_responses']}  \n"
        )
        f.write(f"**Najkrócej:** {ins['shortest_model']}  \n")
        f.write(f"**Najdłużej:** {ins['longest_model']}\n\n")
        f.write(f"**Insight:** {ins['insight']}\n\n")
        f.write(f"**Dlaczego to ważne:** {ins['why_it_matters']}\n\n---\n\n")

print("[✓] Top-5 insights generated")
print(f"[✓] JSON: {OUT_JSON}")
print(f"[✓] MD  : {OUT_MD}")
