---
name: research-workflows
description: "Use when doing knowledge work: literature discovery, arXiv search, blog/RSS monitoring, prediction-market lookup, LLM wiki construction, and research paper drafting/submission."
version: 1.0.0
author: Hermes Agent
license: MIT
platforms: [linux, macos, windows]
metadata:
  hermes:
    tags: [research, arxiv, rss, literature, papers, knowledge-base, prediction-markets]
    related_skills: [youtube-content, model-evaluation-tracking]
---

# Research Workflows

## Overview

Umbrella for research and domain reconnaissance. It covers discovery (arXiv, web, RSS/blog monitoring), structured knowledge bases, prediction-market queries, and turning research into paper drafts or submission packages.

## When to Use

- User asks for academic papers, literature review, or arXiv search.
- User wants to monitor blogs/RSS feeds for changes.
- User wants to build/query an interlinked LLM wiki or knowledge base.
- User asks for Polymarket prices/orderbooks/market history as research evidence.
- User asks to write, revise, or package a research paper.

## Discovery

- Start broad, then narrow with exact author/title/category queries.
- Prefer primary sources and cite IDs/URLs.
- Deduplicate papers/posts; separate facts from interpretation.

## Monitoring

- Use RSS/Atom/blogwatcher flows for recurring source monitoring.
- Report only meaningful changes; avoid noisy full-feed dumps.

## Knowledge Bases

- Use wiki/KB workflows when the task spans many documents or needs later retrieval.
- Preserve provenance for every note/chunk.

## Prediction Markets

- Treat market probabilities as noisy sentiment, not ground truth.
- Include market URL, price, volume/liquidity, and timestamp.

## Paper Writing

- Choose conference/template early.
- Maintain claims→evidence traceability.
- Keep experiments, citations, and reviewer checklist in references/templates rather than one-off notes.

## Verification Checklist

- [ ] Sources/URLs/IDs captured.
- [ ] Current data fetched with tools rather than assumed.
- [ ] Claims are separated from evidence.
- [ ] Deliverable format matches the user request (summary, bib, paper section, monitor report).

## Consolidated Legacy Skills

Absorbed `arxiv`, `blogwatcher`, `llm-wiki`, `polymarket`, and `research-paper-writing`.
