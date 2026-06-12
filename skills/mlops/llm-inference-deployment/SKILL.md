---
name: llm-inference-deployment
description: "Use when downloading, serving, quantizing, or modifying LLMs: Hugging Face Hub, llama.cpp/GGUF, vLLM serving, and refusal/behavior vector surgery."
version: 1.0.0
author: Hermes Agent
license: MIT
platforms: [linux, macos, windows]
metadata:
  hermes:
    tags: [llm, inference, serving, huggingface, llama-cpp, vllm, quantization]
    related_skills: [model-evaluation-tracking]
---

# LLM Inference & Deployment

## Overview

Umbrella for model discovery/download, local GGUF inference, production-ish vLLM serving, quantization choices, and low-level model behavior surgery/abliteration workflows.

## When to Use

- User asks to search/download/upload models or datasets on Hugging Face Hub.
- User asks to run a GGUF model locally with llama.cpp.
- User asks to serve an OpenAI-compatible LLM endpoint with vLLM.
- User asks about quantization, GPU memory, throughput, context length, or deployment troubleshooting.
- User asks to modify refusal behavior or inspect activation directions.

## Modes

### Hugging Face Hub

Use `hf` CLI/API for model/dataset discovery, downloads, uploads, and metadata. Verify license and file sizes before large downloads.

### llama.cpp / GGUF

Use for local CPU/GPU inference, quantized GGUF models, and lightweight OpenAI-compatible server mode.

### vLLM

Use for high-throughput serving, batching, tensor parallelism, and OpenAI-compatible APIs. Check GPU memory and model architecture support first.

### Model Surgery / Abliteration

Treat as experimental and risky. Preserve original weights, record exact layers/directions, and evaluate behavior regressions.

## Verification Checklist

- [ ] Hardware/memory constraints checked.
- [ ] Model license and file sizes considered.
- [ ] Server health endpoint or sample generation tested.
- [ ] Quantization and context settings documented.
- [ ] Modified models are saved separately and evaluated.

## Consolidated Legacy Skills

Absorbed `huggingface-hub`, `llama-cpp`, `serving-llms-vllm`, and `obliteratus`.
