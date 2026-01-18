import json
from collections import defaultdict
import streamlit as st
from pathlib import Path

st.set_page_config(page_title="Mini-1 | BiasLab", layout="wide")

DATA_DIR = Path("reports")
FILES = sorted(DATA_DIR.glob("raw_responses_*.jsonl"))

st.title("Mini-1: szybki rzut oka na dane")
st.caption("Cel: zobaczyć surowe różnice zanim powstaną metryki.")

if not FILES:
    st.error("Nie znaleziono plików raw_responses_*.jsonl w reports/")
    st.stop()

file = st.selectbox("Plik danych:", FILES)
rows = []

with open(file, "r", encoding="utf-8") as f:
    for line in f:
        rows.append(json.loads(line))

st.write(f"Liczba odpowiedzi: **{len(rows)}**")

# --- prosta agregacja ---
by_model = defaultdict(list)
for r in rows:
    text = r.get("answer", "")
    by_model[r["model"]].append(len(text.split()))

summary = [
    {
        "model": model,
        "responses": len(words),
        "avg_words": sum(words) / len(words),
        "min_words": min(words),
        "max_words": max(words),
    }
    for model, words in by_model.items()
]

st.subheader("Długość odpowiedzi (proxy: bogactwo narracji)")
st.table(summary)

st.subheader("Wykres: średnia liczba słów")
st.bar_chart(
    {row["model"]: row["avg_words"] for row in summary}
)

st.subheader("Losowe przykłady odpowiedzi")
sample = st.selectbox("Wybierz model:", list(by_model.keys()))
examples = [r for r in rows if r["model"] == sample][:3]

for i, ex in enumerate(examples, 1):
    with st.expander(f"Przykład {i}"):
        st.markdown(ex["answer"])
