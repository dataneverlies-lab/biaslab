# Methodology

## 1. Research Objective

BiasLab is designed to study **systematic narrative divergence** between large language models (LLMs) when exposed to identical prompts.

The primary objective is **not** to evaluate factual correctness, but to measure and analyze:

- differences in narrative framing,
- variation in response depth and verbosity,
- patterns of caution, evasion, or refusal,
- asymmetries emerging in normatively sensitive topics.

The methodology treats language models as *socio-technical artifacts* whose outputs reflect design choices, training distributions, and alignment constraints.

---

## 2. Core Research Question

> *When multiple language models are asked the same question, where — and how — do their narratives begin to diverge?*

BiasLab operationalizes this question by:
- holding prompts constant,
- varying only the responding model,
- and measuring divergence using reproducible, model-agnostic metrics.

---

## 3. Experimental Design

### 3.1 Prompt Set Construction

Prompts are curated and versioned YAML datasets located in `questions/`.

Design principles:
- identical prompts across all models,
- neutral phrasing unless explicitly testing normative sensitivity,
- separation into thematic sections (e.g. social, ethical, descriptive).

Each prompt is assigned a stable `question_id` to ensure traceability across runs.

---

### 3.2 Model Selection

BiasLab supports heterogeneous models (closed and open, commercial and research).

Models are treated as **black boxes**:
- no access to internal weights,
- no fine-tuning,
- no prompt personalization per model.

This ensures that observed differences emerge from the models themselves, not from experimenter intervention.

---

## 4. Execution Pipeline

Each experimental run follows a fixed pipeline:

1. **Runner**  
   Executes prompts against all selected models and records:
   - raw textual responses,
   - token/word counts,
   - execution metadata.

2. **Auditor**  
   Computes comparative metrics across models for each question, including:
   - inter-model spread,
   - relative response length gaps,
   - indicators of evasion or refusal.

3. **Insight Generator**  
   Ranks questions by divergence and extracts the Top-N most informative cases
   using deterministic, rule-based criteria.

All steps are fully scriptable and reproducible.

---

## 5. Metrics and Measurements

BiasLab intentionally avoids opaque or learned scoring functions.

### 5.1 Primary Metrics

- **Inter-model spread (words)**  
  Difference between shortest and longest responses.

- **Gap ratio**  
  Ratio between extreme response lengths.

- **Short-response indicators**  
  Detection of unusually brief or refusal-like outputs.

These metrics are:
- simple,
- interpretable,
- reproducible across environments.

---

### 5.2 Why Not Semantic Scoring?

BiasLab does **not** rely on:
- embedding similarity,
- LLM-as-a-judge,
- sentiment or toxicity classifiers.

Rationale:
- such methods introduce circularity,
- they depend on other models’ biases,
- they reduce auditability.

BiasLab favors **transparent heuristics** over opaque accuracy claims.

---

## 6. Special Analysis Scopes

Certain runs introduce controlled variations (e.g. demographic descriptors).

These scopes:
- reuse the same pipeline,
- differ only in prompt parameterization,
- are clearly labeled and isolated.

This allows focused analysis without contaminating global results.

---

## 7. Interpretation Layer

BiasLab distinguishes clearly between:

- **measurement** (what differs),
- **interpretation** (why it might differ).

The system provides:
- structured outputs,
- ranked divergence cases,
- contextual metadata.

Interpretation remains the responsibility of the researcher or reader.

---

## 8. Reproducibility

BiasLab is designed for full reproducibility:

- versioned prompts,
- deterministic ranking logic,
- stored intermediate artifacts,
- no hidden parameters.

A third party can re-run an experiment and obtain the same structural results.

---

## 9. Limitations

Known limitations include:
- dependence on surface-level textual features,
- lack of semantic intent modeling,
- sensitivity to prompt phrasing.

These are treated as **explicit design trade-offs**, not oversights.

---

## 10. Research Ethics

BiasLab does not:
- rank models as “better” or “worse”,
- make claims about intent or ideology,
- evaluate compliance with policies.

The methodology is descriptive, not normative.

Ethical considerations are documented separately in `ETHICS.md`.

---

## 11. Intended Use

BiasLab is intended for:
- AI auditability research,
- alignment and safety studies,
- comparative model analysis,
- public-interest transparency.

It is **not** designed as a benchmarking leaderboard or commercial evaluation tool.
