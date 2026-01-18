#!/usr/bin/env python3
"""
BiasLab Runner
==============

Deterministyczny runner do audytu asymetrii narracyjnych w LLM-ach.

Założenia metodologiczne:
- identyczne prompty
- identyczne parametry inferencji
- brak system promptów
- brak analizy w trakcie runu
- pełne logowanie surowych odpowiedzi (JSONL)

Ten plik jest bezpośrednio cytowalny w arXiv (Methods).
"""

import os
import json
import time
import uuid
import yaml
import requests
import argparse
from datetime import datetime, timezone
from pathlib import Path

from dotenv import load_dotenv
load_dotenv()

# =====================================================
# CONFIG — STAŁE EKSPERYMENTALNE
# =====================================================

OPENROUTER_URL = "https://openrouter.ai/api/v1/chat/completions"
API_KEY = os.getenv("OPENROUTER_API_KEY")

# ▶ MAINSTREAM, STABILNA SZÓSTKA (paper-safe)
MODELS = [
    "openai/gpt-4.1",
    "anthropic/claude-3.5-sonnet",
    "meta-llama/llama-3.1-70b-instruct",
    "mistralai/mixtral-8x7b-instruct",
    "qwen/qwen-2.5-72b-instruct",
    "deepseek/deepseek-r1",
]

# ▶ Parametry inferencji (STAŁE)
TEMPERATURE = 0.3
MAX_TOKENS = 600

# ▶ Stabilność
TIMEOUT = 60
RETRIES = 2
SLEEP_BETWEEN_CALLS = 1.2

# =====================================================
# PATHS
# =====================================================

BASE_DIR = Path(__file__).resolve().parent
QUESTIONS_FILE = BASE_DIR / "questions" / "questions_v1.yaml"

RUNS_DIR = BASE_DIR / "runs"
RUNS_DIR.mkdir(exist_ok=True)

# =====================================================
# UTILS
# =====================================================

def now_utc() -> str:
    """Timezone-aware UTC timestamp."""
    return datetime.now(timezone.utc).isoformat()

def load_yaml(path: Path):
    if not path.exists():
        raise FileNotFoundError(f"Questions file not found: {path}")
    with open(path, "r", encoding="utf-8") as f:
        return yaml.safe_load(f)

def write_jsonl(path: Path, obj: dict):
    with open(path, "a", encoding="utf-8") as f:
        f.write(json.dumps(obj, ensure_ascii=False) + "\n")

def call_openrouter(model: str, prompt: str) -> str:
    headers = {
        "Authorization": f"Bearer {API_KEY}",
        "Content-Type": "application/json",
        "X-Title": "BiasLab Runner",
    }

    payload = {
        "model": model,
        "messages": [
            {"role": "user", "content": prompt}
        ],
        "temperature": TEMPERATURE,
        "max_tokens": MAX_TOKENS,
    }

    last_error = None

    for attempt in range(RETRIES + 1):
        try:
            r = requests.post(
                OPENROUTER_URL,
                headers=headers,
                json=payload,
                timeout=TIMEOUT,
            )
            if r.status_code == 200:
                data = r.json()
                return data["choices"][0]["message"]["content"]
            else:
                last_error = f"HTTP {r.status_code}: {r.text}"
        except Exception as e:
            last_error = str(e)

        if attempt < RETRIES:
            time.sleep(2.0)

    raise RuntimeError(f"OpenRouter call failed: {last_error}")

# =====================================================
# RUNNER
# =====================================================

def run():
    if not API_KEY:
        raise RuntimeError("OPENROUTER_API_KEY not found in environment")

    benchmark = load_yaml(QUESTIONS_FILE)

    run_id = f"run_{uuid.uuid4().hex}"
    run_dir = RUNS_DIR / run_id
    run_dir.mkdir()

    out_file = run_dir / "raw_responses.jsonl"

    meta = {
        "run_id": run_id,
        "created_at": now_utc(),
        "models": MODELS,
        "temperature": TEMPERATURE,
        "max_tokens": MAX_TOKENS,
        "questions_file": str(QUESTIONS_FILE),
        "benchmark_version": benchmark.get("version", "unknown"),
        "language": benchmark.get("language", "en"),
    }

    with open(run_dir / "run_meta.json", "w", encoding="utf-8") as f:
        json.dump(meta, f, ensure_ascii=False, indent=2)

    print(f"[+] BiasLab run started: {run_id}")
    print(f"[+] Models: {len(MODELS)}")
    print(f"[+] Output directory: {run_dir}")

    # =========================
    # ITERACJA PO SEKCJACH
    # =========================

    for section in benchmark.get("sections", []):

        # ---------- PUBLIC POLICY ----------
        if section.get("id") == "public_policy":
            for q in section.get("questions", []):
                for model in MODELS:
                    print(f"[*] {model} | {q['id']}")
                    answer = call_openrouter(model, q["prompt"])

                    record = {
                        "run_id": run_id,
                        "timestamp": now_utc(),
                        "benchmark": meta["benchmark_version"],
                        "section": section["id"],
                        "topic": q.get("topic"),
                        "question_id": q["id"],
                        "model": model,
                        "language": meta["language"],
                        "prompt": q["prompt"],
                        "answer": answer,
                    }

                    write_jsonl(out_file, record)
                    time.sleep(SLEEP_BETWEEN_CALLS)

        # ---------- GUARDRAIL ASYMMETRY ----------
        if section.get("id") == "guardrail_asymmetry":
            templates = section["template"]["prompts"]
            groups = section.get("groups", [])

            for pair in groups:
                for which in ("group_a", "group_b"):
                    group_label = pair[which]

                    for tpl in templates:
                        prompt = tpl["prompt"].replace("{GROUP}", group_label)
                        qid = f"{pair['pair_id']}::{tpl['id']}::{which}"

                        for model in MODELS:
                            print(f"[*] {model} | {qid}")
                            answer = call_openrouter(model, prompt)

                            record = {
                                "run_id": run_id,
                                "timestamp": now_utc(),
                                "benchmark": meta["benchmark_version"],
                                "section": section["id"],
                                "pair_id": pair["pair_id"],
                                "which": which,
                                "group": group_label,
                                "question_id": qid,
                                "model": model,
                                "language": meta["language"],
                                "prompt": prompt,
                                "answer": answer,
                            }

                            write_jsonl(out_file, record)
                            time.sleep(SLEEP_BETWEEN_CALLS)

    print("[✓] Run completed successfully")

# =====================================================
if __name__ == "__main__":
    run()
