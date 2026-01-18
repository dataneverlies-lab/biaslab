import json
from pathlib import Path
import re

import streamlit as st
import pandas as pd
from PIL import Image

# =====================================================
# PAGE CONFIG
# =====================================================
st.set_page_config(
    page_title="BiasLab · Narrative Bias Observatory",
    layout="wide",
)

# =====================================================
# CSS
# =====================================================
st.markdown("""
<style>
.block-container { padding-top: 1.1rem; max-width: 1400px; }

.hero-badge {
    font-size: 0.75rem;
    font-weight: 700;
    color: #b00020;
    letter-spacing: 0.08em;
}

.hero-title {
    font-size: 2.15rem;
    font-weight: 800;
    margin-bottom: 0.2rem;
}

.hero-core {
    font-size: 1.05rem;
    font-weight: 700;
    color: #1f1f1f;
    margin-top: 0.35rem;
    margin-bottom: 0.25rem;
}

.hero-sub {
    font-size: 1.02rem;
    color: #555;
    margin-top: 0.15rem;
}

.lang-switch {
    text-align: right;
    font-size: 0.85rem;
    color: #666;
    margin-top: 2.0rem;
}

.logo-wrap img {
    margin-bottom: 0.6rem;
}

.section-title {
    font-size: 1.25rem;
    font-weight: 800;
    margin-top: 0.25rem;
    margin-bottom: 0.35rem;
}

.section-hint {
    color: #666;
    font-size: 0.92rem;
    margin-top: -0.25rem;
    margin-bottom: 0.75rem;
}

.key-insight {
    background: #fafafa;
    border-left: 5px solid #b00020;
    padding: 1rem;
    font-size: 1.02rem;
    border-radius: 10px;
}

.small-pill {
    display:inline-block;
    padding: 0.18rem 0.5rem;
    border-radius: 999px;
    background: #f3f3f3;
    border: 1px solid #e7e7e7;
    font-size: 0.82rem;
    color: #555;
    margin-right: 0.35rem;
}

.model-card {
    border: 1px solid #e5e5e5;
    border-radius: 14px;
    padding: 1.1rem 1.1rem 0.9rem 1.1rem;
    height: 100%;
    background: #fff;
}

.metric-label {
    font-size: 0.8rem;
    color: #666;
    margin-top: 0.55rem;
}

.metric-value {
    font-size: 1.05rem;
    font-weight: 700;
}

.metric-bar {
    background: #eaeaea;
    border-radius: 4px;
    height: 6px;
    margin-top: 0.25rem;
}

.metric-bar-fill {
    background: #b00020;
    height: 6px;
    border-radius: 4px;
}

.hr {
    margin-top: 0.6rem;
    margin-bottom: 0.6rem;
    height: 1px;
    background: #eee;
}

.insight-card {
    border: 1px solid #e8e8e8;
    border-radius: 12px;
    padding: 0.95rem 1rem;
    background: #fff;
    margin-bottom: 0.6rem;
}

.insight-title {
    font-weight: 800;
    margin-bottom: 0.25rem;
}

.insight-meta {
    color: #666;
    font-size: 0.9rem;
    margin-bottom: 0.35rem;
}

.insight-why {
    color: #444;
    font-size: 0.95rem;
    margin-top: 0.35rem;
}

.code-ish {
    font-family: ui-monospace, SFMono-Regular, Menlo, Monaco, Consolas, "Liberation Mono", "Courier New", monospace;
    font-size: 0.9rem;
    color: #333;
}
</style>
""", unsafe_allow_html=True)

# =====================================================
# HELPERS
# =====================================================
def bar(value, max_value=6):
    try:
        v = float(value)
    except Exception:
        v = 0.0
    if max_value and max_value > 0:
        width = max(2, int((v / max_value) * 100))
    else:
        width = 2
    width = min(100, width)
    return f"""
    <div class="metric-bar">
        <div class="metric-bar-fill" style="width:{width}%"></div>
    </div>
    """

def safe_read_json(path: Path):
    with open(path, encoding="utf-8") as f:
        return json.load(f)

def list_available_runs(reports_dir: Path):
    # raport_questions_run_<RUN>.json
    runs = []
    for p in sorted(reports_dir.glob("raport_questions_run_*.json")):
        m = re.search(r"raport_questions_run_(.+)\.json$", p.name)
        if m:
            runs.append(m.group(1))
    # newest first (roughly OK because run_id is hex; keep stable anyway)
    runs = list(dict.fromkeys(runs))
    return runs[::-1] if runs else []

def load_top5(run_id: str, reports_dir: Path):
    # Prefer JSON
    json_path = reports_dir / f"top5_insights_{run_id}.json"
    md_path = reports_dir / f"top5_insights_{run_id}.md"
    if json_path.exists():
        try:
            data = safe_read_json(json_path)
            return ("json", data, json_path)
        except Exception:
            pass
    if md_path.exists():
        try:
            txt = md_path.read_text(encoding="utf-8")
            return ("md", txt, md_path)
        except Exception:
            pass
    return (None, None, None)

# =====================================================
# PATHS
# =====================================================
BASE_DIR = Path(".")
REPORTS_DIR = BASE_DIR / "reports"
ASSETS_DIR = BASE_DIR / "assets"

# =====================================================
# LOAD LOGO
# =====================================================
LOGO_PATH = ASSETS_DIR / "logo.png"
logo = Image.open(LOGO_PATH) if LOGO_PATH.exists() else None

# =====================================================
# HEADER (logo + language + hero)
# =====================================================
col_logo, col_text, col_lang = st.columns([1.7, 6.2, 1.1])

with col_logo:
    if logo:
        st.markdown('<div class="logo-wrap">', unsafe_allow_html=True)
        st.image(logo, width=300)  # większe, czytelniejsze
        st.markdown('</div>', unsafe_allow_html=True)

with col_lang:
    st.markdown('<div class="lang-switch">', unsafe_allow_html=True)
    LANG = st.radio("Language", ["PL", "EN"], horizontal=True, label_visibility="collapsed")
    st.markdown('</div>', unsafe_allow_html=True)

with col_text:
    st.markdown('<div class="hero-badge">NARRATIVE BIAS AUDIT</div>', unsafe_allow_html=True)
    st.markdown('<div class="hero-title">BiasLab · Obserwatorium Asymetrii Narracyjnych</div>', unsafe_allow_html=True)

    if LANG == "PL":
        core = "Model widzi świat oczami zespołu, który zdefiniował jego wszechświat danych."
        sub = "Porównujemy narracje modeli: gdzie te same pytania prowadzą do różnych ram, ostrożności i priorytetów."
    else:
        core = "A model sees the world through the team that defined its universe of data."
        sub = "We compare model narratives: where the same questions trigger different framing, caution, and priorities."

    st.markdown(f'<div class="hero-core">{core}</div>', unsafe_allow_html=True)
    st.markdown(f'<div class="hero-sub">{sub}</div>', unsafe_allow_html=True)

st.divider()

# =====================================================
# STEP 0: SELECT RUN (the artifact you are viewing)
# =====================================================
st.markdown(f"<div class='section-title'>{'1) Wybierz run (zestaw wyników)' if LANG=='PL' else '1) Select a run (result bundle)'}</div>", unsafe_allow_html=True)

available_runs = list_available_runs(REPORTS_DIR)
if not available_runs:
    st.error("Brak plików raportu w reports/: raport_questions_run_*.json")
    st.stop()

run_id = st.selectbox(
    "Run ID",
    options=available_runs,
    index=0,
    help="Wybierasz konkretny zestaw wyników (runner → auditor → insight generator)."
)

REPORT_FILE = REPORTS_DIR / f"raport_questions_run_{run_id}.json"
METRICS_FILE = REPORTS_DIR / f"metrics_questions_run_{run_id}.csv"

# optional (legacy) race file for model profiles
RACE_FILE = REPORTS_DIR / "race01_metrics_v4.csv"

# Load report JSON
if not REPORT_FILE.exists():
    st.error(f"Brak raportu: {REPORT_FILE}")
    st.stop()
report = safe_read_json(REPORT_FILE)

questions = report.get("questions", {})
meta = report.get("meta", {})

# Load metrics CSV (auditor output)
metrics_df = None
if METRICS_FILE.exists():
    metrics_df = pd.read_csv(METRICS_FILE)
else:
    st.warning(f"Brak metrics CSV dla tego runa: {METRICS_FILE.name} (Overview będzie ograniczone).")

# Load optional race metrics
race_df = pd.read_csv(RACE_FILE) if RACE_FILE.exists() else None

# Meta line (nice and short)
if LANG == "PL":
    meta_line = f"{meta.get('questions_total', len(questions))} pytań · {len(meta.get('models', []))} modeli · {meta.get('created_at', '')}"
else:
    meta_line = f"{meta.get('questions_total', len(questions))} questions · {len(meta.get('models', []))} models · {meta.get('created_at', '')}"

st.caption(meta_line)

st.markdown("<div class='hr'></div>", unsafe_allow_html=True)

# =====================================================
# STEP 1: SCOPE (Global vs race_01) + short explanation
# =====================================================
st.markdown(f"<div class='section-title'>{'2) Zakres analizy' if LANG=='PL' else '2) Analysis scope'}</div>", unsafe_allow_html=True)

scope = st.radio(
    "Zakres analizy" if LANG == "PL" else "Analysis scope",
    ["Global", "race_01"],
    horizontal=True,
)

if LANG == "PL":
    scope_expl = (
        "Flow jest prosty: **runner** zbiera odpowiedzi, **auditor** liczy metryki różnic, "
        "a generator insightów wybiera Top-5 najbardziej rozbieżnych pytań."
    )
else:
    scope_expl = (
        "The flow is simple: **runner** collects answers, **auditor** computes divergence metrics, "
        "and the insight generator selects the Top-5 most divergent questions."
    )
st.markdown(f"<div class='section-hint'>{scope_expl}</div>", unsafe_allow_html=True)

st.markdown("<div class='hr'></div>", unsafe_allow_html=True)

# =====================================================
# STEP 2: KEY INSIGHTS (Top-5 + meta-insight) FIRST (more intuitive)
# =====================================================
st.markdown(f"<div class='section-title'>{'3) Key insights' if LANG=='PL' else '3) Key insights'}</div>", unsafe_allow_html=True)

# A) Scope-specific single insight (your existing one)
if scope == "race_01":
    if LANG == "PL":
        headline_insight = (
            "Gdy modele opisują **Black people**, dominuje narracja systemowa i strukturalna. "
            "Dla **White people** te same modele częściej przechodzą na język uogólnień i symetrii."
        )
    else:
        headline_insight = (
            "When models describe **Black people**, systemic/structural framing dominates. "
            "For **White people**, the same models more often shift toward generalizations and symmetry language."
        )
else:
    if LANG == "PL":
        headline_insight = (
            "Różnice między modelami nie polegają tylko na długości odpowiedzi — "
            "często chodzi o **domyślne ramy narracyjne** (co model uznaje za „ważne”)."
        )
    else:
        headline_insight = (
            "Differences between models are not only about response length — "
            "they often reflect **default narrative framing** (what the model treats as “important”)."
        )

st.markdown(
    f"<div class='key-insight'><strong>{'Headline:' if LANG=='EN' else 'Najważniejsze:'}</strong> {headline_insight}</div>",
    unsafe_allow_html=True
)

st.markdown("<div style='height:0.55rem'></div>", unsafe_allow_html=True)

# B) Top-5 insights artifact for the run
fmt, top5_data, top5_path = load_top5(run_id, REPORTS_DIR)

if fmt is None:
    if LANG == "PL":
        st.info("Brak Top-5 dla tego runa. Uruchom generator: `python top5_insights.py <run_id>`.")
    else:
        st.info("No Top-5 for this run yet. Generate it: `python top5_insights.py <run_id>`.")
else:
    # Prefer JSON format if present; otherwise render markdown.
    if fmt == "json":
        meta_insight = top5_data.get("meta_insight") or top5_data.get("metaInsight") or ""
        items = top5_data.get("items") or top5_data.get("top5") or []

        if meta_insight:
            st.markdown(
                f"<div class='insight-card'><div class='insight-title'>Meta-insight</div>"
                f"<div class='insight-meta'>{meta_insight}</div></div>",
                unsafe_allow_html=True
            )

        st.markdown(f"<div class='section-hint'>{'Top-5 najbardziej rozbieżnych pytań (rule-based, reprodukowalne).' if LANG=='PL' else 'Top-5 most divergent questions (rule-based, reproducible).'} "
                    f"<span class='small-pill'>source: {top5_path.name}</span></div>", unsafe_allow_html=True)

        for idx, it in enumerate(items[:5], start=1):
            title = it.get("title", f"Insight {idx}")
            qid = it.get("question_id", "")
            section = it.get("section", "")
            prompt = it.get("prompt", "")
            spread = it.get("spread_words", it.get("spread", None))
            gap = it.get("gap_ratio", it.get("gap", None))
            short = it.get("short_responses", it.get("short", None))
            shortest = it.get("shortest_model", "")
            longest = it.get("longest_model", "")
            insight_txt = it.get("insight", "")
            why_txt = it.get("why_it_matters", it.get("why", ""))

            st.markdown(
                "<div class='insight-card'>"
                f"<div class='insight-title'>{idx}. {title}</div>"
                f"<div class='insight-meta'><span class='code-ish'>{qid}</span> · {section}</div>"
                f"<div><span class='small-pill'>spread: {spread}</span>"
                f"<span class='small-pill'>gap: {gap}</span>"
                f"<span class='small-pill'>short: {short}</span></div>"
                f"<div style='margin-top:0.5rem'><strong>{'Pytanie' if LANG=='PL' else 'Question'}:</strong> {prompt}</div>"
                f"<div style='margin-top:0.35rem'><strong>{'Najkrócej' if LANG=='PL' else 'Shortest'}:</strong> {shortest} "
                f"· <strong>{'Najdłużej' if LANG=='PL' else 'Longest'}:</strong> {longest}</div>"
                f"<div style='margin-top:0.5rem'><strong>Insight:</strong> {insight_txt}</div>"
                f"<div class='insight-why'><strong>{'Dlaczego to ważne' if LANG=='PL' else 'Why it matters'}:</strong> {why_txt}</div>"
                "</div>",
                unsafe_allow_html=True
            )
    else:
        # Markdown fallback
        st.markdown(f"<div class='section-hint'>Top-5 z pliku: <span class='small-pill'>{top5_path.name}</span></div>", unsafe_allow_html=True)
        st.markdown(top5_data)

st.markdown("<div class='hr'></div>", unsafe_allow_html=True)

# =====================================================
# STEP 3: MODEL PROFILES
# =====================================================
st.markdown(f"<div class='section-title'>{'4) Profile modeli' if LANG=='PL' else '4) Model profiles'}</div>", unsafe_allow_html=True)

if LANG == "PL":
    st.markdown("<div class='section-hint'>To jest szybka „karta modelu” — heurystyki podglądowe. Dla race_01 używamy race01_metrics_v4.csv (jeśli istnieje).</div>", unsafe_allow_html=True)
else:
    st.markdown("<div class='section-hint'>Quick model cards — preview heuristics. For race_01 we use race01_metrics_v4.csv (if present).</div>", unsafe_allow_html=True)

models = meta.get("models", [])
if not models:
    st.warning("Brak listy modeli w raporcie meta.")
else:
    # dynamic columns (better for 6 models)
    n = len(models)
    per_row = 3 if n >= 3 else n
    rows_models = [models[i:i+per_row] for i in range(0, n, per_row)]

    for row in rows_models:
        cols = st.columns(per_row)
        for col, model in zip(cols, row):
            with col:
                st.markdown('<div class="model-card">', unsafe_allow_html=True)
                st.markdown(f"### 🤖 {model}")

                if race_df is not None and scope == "race_01":
                    subdf = race_df[race_df["model"] == model]
                    depth = float(subdf["systemic_score"].mean()) if len(subdf) else 0.0
                    evas = float(subdf["soft_evasion"].mean()) if len(subdf) else 0.0
                    refusals = float(subdf["refusal_like"].mean()) if len(subdf) else 0.0
                else:
                    # placeholder global (zostawione jak było)
                    depth, evas, refusals = 3.0, 0.2, 0.0

                st.markdown("<div class='metric-label'>Narrative depth</div>", unsafe_allow_html=True)
                st.markdown(bar(depth), unsafe_allow_html=True)
                st.markdown(f"<div class='metric-value'>{depth:.2f}</div>", unsafe_allow_html=True)

                st.markdown("<div class='metric-label'>Soft evasion</div>", unsafe_allow_html=True)
                st.markdown(bar(evas), unsafe_allow_html=True)
                st.markdown(f"<div class='metric-value'>{evas:.2f}</div>", unsafe_allow_html=True)

                st.markdown("<div class='metric-label'>Short / refusals</div>", unsafe_allow_html=True)
                st.markdown(bar(refusals, max_value=1), unsafe_allow_html=True)
                st.markdown(
                    f"<div class='metric-value'>{'LOW' if refusals < 0.2 else 'HIGH'}</div>",
                    unsafe_allow_html=True
                )

                st.markdown("</div>", unsafe_allow_html=True)

st.markdown("<div class='hr'></div>", unsafe_allow_html=True)

# =====================================================
# STEP 4: OVERVIEW (metrics + bar chart)
# =====================================================
st.markdown(f"<div class='section-title'>{'5) Overview (metryki przekrojowe)' if LANG=='PL' else '5) Overview (cross-metrics)'}</div>", unsafe_allow_html=True)

if metrics_df is None:
    # fallback to legacy report json (still show something)
    rows = []
    for qid, q in questions.items():
        try:
            spread = q["metrics"]["inter_model_spread_words"]
        except Exception:
            spread = None
        if spread is not None:
            rows.append({"question_id": qid, "spread_words": spread})
    df_over = pd.DataFrame(rows)
else:
    df_over = metrics_df.copy()

if df_over.empty:
    st.warning("Brak danych do overview.")
else:
    # normalize column names (in case)
    if "spread_words" not in df_over.columns and "Spread" in df_over.columns:
        df_over["spread_words"] = df_over["Spread"]

    # Display headline metrics
    spread_col = "spread_words" if "spread_words" in df_over.columns else df_over.columns[0]

    c1, c2, c3, c4 = st.columns(4)
    c1.metric("Średni spread" if LANG == "PL" else "Average spread", f"{df_over[spread_col].mean():.1f}")
    c2.metric("Max spread", f"{df_over[spread_col].max()}")
    if "gap_ratio" in df_over.columns:
        c3.metric("Max gap" if LANG == "PL" else "Max gap", f"{df_over['gap_ratio'].max():.2f}×")
    else:
        c3.metric("Max gap" if LANG == "PL" else "Max gap", "—")
    if "short_responses" in df_over.columns:
        c4.metric("Krótkie odpowiedzi" if LANG == "PL" else "Short responses", int(df_over["short_responses"].sum()))
    else:
        c4.metric("Krótkie odpowiedzi" if LANG == "PL" else "Short responses", "—")

    # Chart
    chart_df = df_over[["question_id", spread_col]].copy()
    chart_df = chart_df.sort_values(spread_col, ascending=False)
    chart_df = chart_df.rename(columns={spread_col: "spread_words"}).set_index("question_id")

    st.bar_chart(chart_df)

st.markdown("<div class='hr'></div>", unsafe_allow_html=True)

# =====================================================
# STEP 5: QUESTION BROWSER (so user can inspect the actual material)
# =====================================================
st.markdown(f"<div class='section-title'>{'6) Pytania i odpowiedzi (źródło prawdy)' if LANG=='PL' else '6) Questions & answers (ground truth)'}</div>", unsafe_allow_html=True)

if LANG == "PL":
    st.markdown("<div class='section-hint'>Tu sprawdzasz konkret: prompt oraz odpowiedzi wszystkich modeli. Insighty mają sens tylko, jeśli można je zweryfikować tutaj.</div>", unsafe_allow_html=True)
else:
    st.markdown("<div class='section-hint'>Verify specifics here: the prompt and all model answers. Insights only matter if you can audit them here.</div>", unsafe_allow_html=True)

# Build a simple question list
q_items = []
for qid, q in questions.items():
    sec = q.get("section", "")
    q_items.append((qid, sec))
q_items.sort(key=lambda x: x[0])

selected_qid = st.selectbox(
    "Question ID",
    options=[qid for qid, _ in q_items],
    index=0 if q_items else None
)

if selected_qid:
    q = questions[selected_qid]
    prompt = q.get("prompt", "")
    sec = q.get("section", "")
    hint = q.get("insight_hint", "")

    st.markdown(f"<span class='small-pill'>section: {sec}</span> <span class='small-pill'>id: {selected_qid}</span>", unsafe_allow_html=True)

    if hint:
        st.markdown(f"<div class='key-insight'><strong>{'Hint:' if LANG=='EN' else 'Podpowiedź:'}</strong> {hint}</div>", unsafe_allow_html=True)

    st.markdown(f"**{'Pytanie (prompt)' if LANG=='PL' else 'Prompt'}:** {prompt}")

    # Responses
    responses = q.get("responses", {})
    if not responses:
        st.warning("Brak odpowiedzi w raporcie dla tego pytania.")
    else:
        # order models consistently
        ordered_models = meta.get("models", list(responses.keys()))
        for m in ordered_models:
            if m not in responses:
                continue
            ans = responses[m].get("answer", "")
            words = responses[m].get("words", None)

            with st.expander(f"{m} · {words} words" if words is not None else m, expanded=False):
                st.write(ans)

# =====================================================
# FOOTER
# =====================================================
st.divider()
st.caption("BiasLab · Data Never Lies · Narrative Bias Observatory")
