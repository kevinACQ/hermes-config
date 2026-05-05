---
name: claude-knowledge-base-search
category: note-taking
description: Search Kevin's Claude knowledge base using the local SQLite/Markdown index and return grounded article results.
---

# Claude Knowledge Base Search

Use when Kevin asks to search his knowledge base, find articles/resources in the KB, or retrieve saved KB entries by topic.

## Known locations

- Knowledge base root: `/Users/kevin/projects/cog-config/knowledge-base`
- Symlinks:
  - `/Users/kevin/.claude/knowledgebase`
  - `/Users/kevin/.hermes/knowledgebase`
- SQLite index: `/Users/kevin/projects/cog-config/knowledge-base/.kb-index.sqlite`
- Human index: `/Users/kevin/projects/cog-config/knowledge-base/INDEX.md`
- Search script: `/Users/kevin/.hermes/scripts/kb_search.py`
- Claude ingest skill: `/Users/kevin/.claude/skills/kb-add/SKILL.md`
- Claude search skill: `/Users/kevin/.claude/skills/kb-search/SKILL.md`

## Workflow

1. Prefer the KB search script/index over memory when the user asks what is in the KB.
2. Query the KB with the user's topic and related synonyms if needed.
3. Return article title, source/author when available, URL when available, and KB path.
4. Separate strong matches from weak/secondary matches.
5. If expected resources are absent, say they are not saved in the KB rather than implying they do not exist.

## Example query

For “evals for LLMs”, expected strong KB resources include:

- OpenAI Evals — `openai/2026-05-04__web-article__openai-evals.md`
- Hamel Husain — `hamel-husain/2026-05-04__web-article__using-llm-as-a-judge-for-evaluation-a-complete-guide.md`
- Hamel Husain — `hamel-husain/2026-05-04__web-article__a-field-guide-to-rapidly-improving-ai-products.md`
- Hamel Husain — `hamel-husain/2026-05-04__web-article__your-ai-product-needs-evals.md`
- Anthropic Prompt Evaluations Course — `anthropic/2026-05-04__web-article__anthropic-prompt-evaluations-course.md`

## Pitfalls

- Do not answer KB search questions from chat memory alone.
- Do not confuse Hermes session history with the KB.
- GitHub repos should be ingested as concise reference notes unless the user explicitly wants raw repo content.
- Permission requests are last resort: first use local scripts/files/indexes already available.

## Verification

Before finalizing, verify that returned paths exist in the KB or are present in the index output.