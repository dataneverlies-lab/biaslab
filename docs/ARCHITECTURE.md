# BiasLab — Architecture & Research Pipeline

## 1. Purpose of the Architecture

BiasLab is a research system designed for **reproducible auditing of narrative asymmetries in large language models**.  
The architecture explicitly separates:

- data generation (model responses),
- metric computation,
- insight selection,
- presentation and audit layers.

The goal is to enable **independent verification of results**, scientific publication (e.g. arXiv), and long-term development as an Internet public good (NGI / open science).

---

## 2. High-level Data Flow

The BiasLab pipeline consists of five logical stages:

1. **Questions → Runner**
2. **Runner → Raw responses**
3. **Raw responses → Auditor**
4. **Auditor → Metrics & Top-5 insights**
5. **Metrics → Dashboard / Publication**

Each stage produces explicit, persistent artifacts on disk in a deterministic manner.

---

## 3. Question Layer

**Location:** `questions/`

- Questions are defined in YAML files.
- Each question includes:
  - a unique identifier,
  - a thematic section,
  - the prompt text,
  - an optional `insight_hint` (interpretive guidance).

Questions are **static and versioned**, enabling comparisons across experimental runs over time.

---

## 4. Runner — Collecting Model Responses

**File:** `runner.py`  
**Output:** `runs/<run_id>/raw.json`

The Runner is responsible for:

- asking **the same questions** to all models,
- storing raw responses without interpretation,
- recording metadata (timestamp, models, run identifier).

The Runner:
- does not compute metrics,
- does not filter content,
- does not interpret responses.

This layer is **purely observational**.

---

## 5. Auditor — Computing Divergence Metrics

**File:** `auditor.py`  
**Outputs:**  
- `reports/raport_questions_run_<id>.json`  
- `metrics_questions_run_<id>.csv`

The Auditor analyzes responses and computes metrics such as:

- narrative length (word count),
- inter-model spread,
- soft evasion indicators,
- shortening / refusal signals.

The Auditor:
- is deterministic,
- does not use LLMs,
- relies on simple, auditable rules.

This is the **scientific core** of the project.

---

## 6. Top-5 Insight Generator

**File:** `top5_insights.py`  
**Output:** `top5_insights_<run_id>.json` or `.md`

This component:

- selects questions with the highest narrative divergence,
- produces concise, structured insights,
- preserves full traceability to source data.

The Top-5 insights:
- are not model-generated interpretations,
- are research artifacts,
- serve as a bridge between metrics and publication.

---

## 7. Visualization and Audit Layer

**File:** `streamlit_app_v2.py`

The dashboard serves as:

- an exploratory interface,
- an audit tool,
- a demonstration surface for reviewers and researchers.

Key UX principles:
- a user understands the project’s purpose within ~20 seconds,
- observations are clearly separated from interpretation,
- every claim is traceable to raw data.

The dashboard **does not generate data** — it only presents existing artifacts.

---

## 8. Research Artifacts and Reproducibility

BiasLab persists all critical artifacts:

- raw model responses,
- computed metrics,
- generated insights,
- run configurations.

As a result:
- every result can be reproduced,
- runs can be compared across time,
- the repository is suitable for long-term archival (e.g. Zenodo, arXiv).

---

## 9. Design Principles

- **Separation of concerns** — each layer has a single responsibility.
- **No hidden state** — all state is explicit and persisted.
- **No black boxes** — no opaque LLM-based interpretation layers.
- **Open science by default** — code and data are auditable.

---

## 10. Project Status

BiasLab is a project that is:

- research-first,
- open source,
- oriented toward the Internet commons.

The architecture is stable and ready for:
- scientific publication,
- grant applications (NGI / NLnet),
- extension by the research community.

---

**Data Never Lies.  
Narratives Do.**
