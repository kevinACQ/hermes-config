---
name: model-evaluation-tracking
description: "Use when evaluating ML/LLM systems or tracking experiments: lm-eval-harness benchmarks, API model evals, distributed runs, W&B logging, sweeps, artifacts, and dashboards."
version: 1.0.0
author: Hermes Agent
license: MIT
platforms: [linux, macos, windows]
metadata:
  hermes:
    tags: [evaluation, llm-benchmarks, wandb, experiments, sweeps, artifacts]
    related_skills: [huggingface-hub]
---

# Model Evaluation & Experiment Tracking

## Overview

Umbrella for running model evaluations and recording experiment evidence. Combine benchmark harnesses with tracking systems so results are reproducible, comparable, and inspectable.

## When to Use

- User asks to benchmark an LLM on MMLU/GSM8K/custom tasks.
- User asks to evaluate API-hosted or local models.
- User wants distributed or batch evaluation runs.
- User wants W&B runs, sweeps, artifacts, dashboards, or model registry workflows.

## Evaluation Workflow

1. Define task, dataset, metric, model, tokenizer, and generation settings.
2. Pin versions and seeds where possible.
3. Run a smoke test before a full benchmark.
4. Capture stdout, config, and result JSON/CSV.
5. Log to W&B or equivalent tracking if the result should be compared later.
6. Summarize metrics plus caveats (sample size, prompt format, contamination risk).

## lm-eval Harness

- Use for standardized academic-style LLM benchmarks.
- Prefer small `--limit` smoke tests before full runs.
- Store task config and exact command with results.

## W&B Tracking

- Use for experiment metadata, metrics, artifacts, sweeps, and dashboards.
- Avoid logging secrets or raw private data.
- Treat run URLs/artifact IDs as verification handles.

## Verification Checklist

- [ ] Exact eval command/config captured.
- [ ] Smoke test succeeded before expensive run.
- [ ] Results are saved and, if requested, logged to tracking.
- [ ] Final answer includes metrics and file/run URLs.

## Consolidated Legacy Skills

Absorbed `evaluating-llms-harness` and `weights-and-biases`.
