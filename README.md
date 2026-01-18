BiasLab

Narrative Bias Observatory for Large Language Models

A model sees the world through the team that defined its universe of data.

BiasLab is an open research framework for measuring and comparing narrative divergence between large language models (LLMs) when answering identical questions.

Rather than evaluating factual correctness, BiasLab focuses on how models frame meaning, responsibility, risk, and social context — especially in normatively sensitive scenarios.

⸻

What BiasLab measures

BiasLab analyzes inter-model narrative asymmetries, including:
	•	differences in response length and narrative depth
	•	shifts in framing (systemic vs individual, neutral vs normative)
	•	patterns of caution, evasion, or refusal
	•	divergences emerging in socially or politically sensitive questions

The core premise is simple:

If models receive the same prompts, systematic differences in their narratives reveal implicit priorities, constraints, and alignment strategies embedded during training and deployment.

⸻

Why this matters

Narrative differences are not random artifacts.
They consistently emerge most strongly in questions involving:
	•	social groups and identity
	•	platform responsibility
	•	harm, safety, or moderation
	•	normatively loaded scenarios

These divergences are relevant for:
	•	AI alignment and safety research
	•	transparency and auditability of deployed models
	•	public-interest oversight
	•	policy and regulatory discussions

BiasLab provides a reproducible, model-agnostic methodology for observing and analyzing these effects.

⸻

Method overview

BiasLab follows a transparent, auditable pipeline:
	1.	Runner
Executes the same prompt set across multiple language models and stores raw responses.
	2.	Auditor
Computes quantitative divergence metrics, including:
	•	inter-model spread (word count differences)
	•	gap ratios (longest vs shortest narrative)
	•	frequency of short or refusal-like responses
	3.	Sanity checks
Validate raw outputs and derived metrics for consistency.
	4.	Insight generator
Selects the Top-5 most divergent questions using deterministic, rule-based scoring (no LLM interpretation).
	5.	Dashboard
An interactive Streamlit interface for inspection, comparison, and audit.

⸻

Repository structure

biaslab/
├── runner.py
├── auditor.py
├── top5_insights.py
├── sanity_check_raw.py
├── sanity_check_metrics.py
├── analyze_race01_v3.py
├── streamlit_app_v2.py
├── questions/
├── reports/
├── assets/
├── requirements.txt
└── README.md

⸻

Reproducibility

BiasLab is designed for full reproducibility:
	•	deterministic metrics
	•	explicit scoring rules
	•	no LLM-based interpretation in analysis steps
	•	all outputs derived from versioned inputs

Minimal workflow:

pip install -r requirements.txt
python runner.py
python auditor.py
python top5_insights.py <run_id>
streamlit run streamlit_app_v2.py

⸻

Research status
	•	Functional research prototype
	•	Deterministic metrics and insight selection
	•	Interactive audit dashboard
	•	Open-source, public codebase

Current work focuses on:
	•	expanding prompt sets
	•	refining narrative divergence metrics
	•	preparing formal academic publication

⸻

License

This project is released under an open-source license.
All research artifacts are intended for open access and public scrutiny.

⸻

Citation

A formal citation entry and arXiv preprint will be added.
Until then, please reference this repository directly.

⸻

Philosophy

BiasLab is developed in the spirit of:
	•	open science
	•	public-interest AI research
	•	transparency over persuasion
	•	measurement over speculation

The goal is not to rank models as better or worse, but to make narrative differences visible, inspectable, and discussable.
