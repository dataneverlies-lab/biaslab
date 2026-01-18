
# biaslab
BiasLab is an open, reproducible research framework for auditing narrative divergence and normative bias in large language models by comparing how different models respond to the same questions in socially sensitive and normative contexts.

# BiasLab — Narrative Bias Observatory

BiasLab is an open research framework for auditing narrative divergence
between large language models.

The system runs the same structured question sets across multiple models
and analyzes where their narratives begin to diverge — not only in length,
but in framing, caution, responsibility attribution, and systemic focus.

## What this repository contains

- `runner.py` — executes controlled question runs across models
- `auditor.py` — computes inter-model divergence metrics
- `top5_insights.py` — extracts the most divergent narrative cases
- `sanity_check_*.py` — robustness and consistency checks
- `streamlit_app_v2.py` — interactive audit dashboard
- `questions/` — curated, versioned research question sets

## Research focus

BiasLab focuses on:
- narrative framing asymmetries
- normative sensitivity
- model-specific risk and responsibility defaults
- reproducible, rule-based insight extraction

## Reproducibility

This repository contains **code and methodology only**.
Runtime outputs (reports, runs, datasets) are intentionally excluded.

## License

Open-source. See LICENSE file.

