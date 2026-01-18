#!/usr/bin/env python3
import json
from pathlib import Path
from collections import defaultdict
from datetime import datetime, timezone
import csv
import sys

# =========================
# CONFIG
# =========================
BASE_DIR = Path(__file__).resolve().parent
RUNS_DIR = BASE_DIR / "runs"
REPORTS_DIR = BASE_DIR / "reports"

SHORT_RESPONSE_THRESHOLD = 50  # techniczna definicja „ubogiej narracji”

# =========================
# UTILS
# =========================
def now_utc():
    return datetime.now(timezone.utc).isoformat()

def word_count(text: str) -> int:
    return len(text.split())

# =========================
# SELECT RUN
# =========================
if len(sys.argv) < 2:
    raise RuntimeError(
        "Podaj run_id.\n"
        "Przykład: python auditor.py run_20260116_082714"
    )

RUN_ID = sys.argv[1]
RUN_DIR = RUNS_DIR / RUN_ID

RAW_FILE = RUN_DIR / "raw_responses.jsonl"

if not RAW_FILE.exists():
    raise FileNotFoundError(f"Brak pliku: {RAW_FILE}")

REPORTS_DIR.mkdir(parents=True, exist_ok=True)

# =========================
# LOAD RAW DATA
# =========================
rows = []
with open(RAW_FILE, "r", encoding="utf-8") as f:
    for line in f:
        rows.append(json.loads(line))

if not rows:
    raise RuntimeError("Plik raw_responses.jsonl jest pusty")

# =========================
# RE-AGGREGATION (QUESTION-CENTRIC)
# =========================
by_question = defaultdict(lambda: {
    "section": None,
    "prompt": None,
    "meta": {},
    "responses": {}
})

models_set = set()

for r in rows:
    qid = r["question_id"]
    model = r["model"]
    answer = r.get("answer", "")

    models_set.add(model)

    by_question[qid]["section"] = r.get("section")
    by_question[qid]["prompt"] = r.get("prompt")

    # zachowujemy dodatkowe pola dla guardrail
    for k in ("pair_id", "group", "which"):
        if k in r:
            by_question[qid]["meta"][k] = r[k]

    by_question[qid]["responses"][model] = {
        "words": word_count(answer),
        "answer": answer
    }

# =========================
# METRICS PER QUESTION
# =========================
questions_out = {}
metrics_rows = []

for qid, qdata in by_question.items():
    responses = qdata["responses"]

    # pomijamy pytania niepełne
    if len(responses) < 2:
        continue

    word_map = {m: d["words"] for m, d in responses.items()}

    longest_model = max(word_map, key=word_map.get)
    shortest_model = min(word_map, key=word_map.get)

    max_words = word_map[longest_model]
    min_words = word_map[shortest_model]

    spread = max_words - min_words
    gap_ratio = round(max_words / min_words, 2) if min_words > 0 else None

    short_models = [
        m for m, w in word_map.items()
        if w < SHORT_RESPONSE_THRESHOLD
    ]

    metrics = {
        "inter_model_spread_words": spread,
        "longest_model": longest_model,
        "shortest_model": shortest_model,
        "relative_gap_ratio": gap_ratio,
        "short_response_models": short_models,
    }

    questions_out[qid] = {
        "section": qdata["section"],
        "prompt": qdata["prompt"],
        "meta": qdata["meta"],
        "responses": responses,
        "metrics": metrics,
    }

    # CSV row (do rankingów i dalszych analiz)
    metrics_rows.append({
        "run_id": RUN_ID,
        "question_id": qid,
        "section": qdata["section"],
        "spread_words": spread,
        "gap_ratio": gap_ratio,
        "short_responses": len(short_models),
    })

# =========================
# WRITE REPORT JSON
# =========================
report = {
    "meta": {
        "run_id": RUN_ID,
        "created_at": now_utc(),
        "models": sorted(models_set),
        "questions_total": len(questions_out),
        "short_response_threshold": SHORT_RESPONSE_THRESHOLD,
    },
    "questions": questions_out
}

OUT_JSON = REPORTS_DIR / f"raport_questions_{RUN_ID}.json"
with open(OUT_JSON, "w", encoding="utf-8") as f:
    json.dump(report, f, indent=2, ensure_ascii=False)

# =========================
# WRITE METRICS CSV
# =========================
OUT_CSV = REPORTS_DIR / f"metrics_questions_{RUN_ID}.csv"
with open(OUT_CSV, "w", encoding="utf-8", newline="") as f:
    writer = csv.DictWriter(
        f,
        fieldnames=metrics_rows[0].keys()
    )
    writer.writeheader()
    writer.writerows(metrics_rows)

print("[✓] Audit zakończony")
print(f"[✓] JSON: {OUT_JSON}")
print(f"[✓] CSV : {OUT_CSV}")
print(f"[i] Modele: {', '.join(sorted(models_set))}")
