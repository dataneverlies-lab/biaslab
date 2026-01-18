# Limitations

BiasLab is designed as a reproducible research framework for analyzing narrative divergence across language models. While the system is intentionally conservative in its methodology, several limitations should be explicitly acknowledged.

## 1. Scope of Questions and Domains

The current analyses are limited to a predefined set of questions and thematic sections.  
Although questions are curated to expose normatively sensitive and socially salient contexts, the results should not be interpreted as exhaustive or universal representations of model behavior across all domains.

Different prompts, phrasings, or cultural contexts may yield different divergence patterns.

## 2. Focus on Narrative Structure, Not Ground Truth

BiasLab does **not** evaluate factual correctness, moral validity, or ethical desirability of model responses.  
All metrics operate on **narrative form**, including length, framing, avoidance strategies, and response asymmetry.

As a result, the framework detects *how* models respond differently, not *which response is correct*.

## 3. Model and Version Dependence

Results are inherently dependent on:
- the specific models evaluated,
- their versions at the time of execution,
- and the inference configurations used.

BiasLab does not claim temporal stability of findings. Re-running the same analysis on updated models may produce materially different results, which is considered a feature rather than a flaw.

## 4. Heuristic Metrics

Metrics such as narrative depth, soft evasion, refusal likelihood, and inter-model spread are heuristic by design.  
They are intentionally simple, interpretable, and reproducible, but they do not capture all dimensions of narrative behavior.

Subtle rhetorical strategies, tone shifts, or implicit framing choices may not be fully reflected in quantitative scores.

## 5. Absence of Human Judgment in Interpretation

BiasLab deliberately avoids LLM-based interpretation or automated semantic judgment of results.  
All higher-level interpretations presented in insights or dashboards are authored by human researchers.

While this reduces automation bias, it also means that interpretive layers are not scalable without additional human review.

## 6. Non-Prescriptive Use

BiasLab is an observational and diagnostic tool.  
It is not intended to prescribe policy decisions, evaluate compliance, or rank models in terms of ethical quality.

Any downstream use of BiasLab results for governance, regulation, or public communication should be accompanied by additional contextual analysis.

## 7. Dataset and Cultural Bias

The selection of questions and analytical focus reflects the cultural, linguistic, and normative assumptions of the research team.  
Although this is made explicit, it remains a structural limitation shared by all interpretive research systems.

BiasLab encourages independent replication with alternative question sets and cultural framings.

---

By making these limitations explicit, BiasLab aims to support responsible interpretation, reproducibility, and constructive reuse of its methods and findings.
