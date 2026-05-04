---
name: kevin-knowledge-base
description: Add articles, URLs, videos, or pasted content to Kevin's Claude knowledge base; discover the canonical folder/symlinks and use Claude's kb-add workflow when available.
---

# Kevin Knowledge Base

Use this when Kevin asks to save/add/ingest articles, URLs, videos, or other source material to his knowledge base/wiki/KB.

## Canonical location

Kevin's Claude knowledge base lives at:

```text
/Users/kevin/projects/cog-config/knowledge-base
```

Convenience symlinks may exist at:

```text
/Users/kevin/.claude/knowledgebase
/Users/kevin/.hermes/knowledgebase
```

Claude's source skill is:

```text
/Users/kevin/.claude/skills/kb-add/SKILL.md
```

Read that file before ingesting, because it defines the exact folder structure, filename convention, and frontmatter schema.

## Quick discovery / repair

If unsure where the KB is, check in this order:

1. `/Users/kevin/projects/cog-config/knowledge-base`
2. `/Users/kevin/.claude/knowledgebase`
3. `/Users/kevin/.claude/knowledge-base`
4. `/Users/kevin/.hermes/knowledgebase`

If the canonical folder exists but symlinks are missing, recreate them:

```bash
ln -s /Users/kevin/projects/cog-config/knowledge-base /Users/kevin/.claude/knowledgebase
ln -s /Users/kevin/projects/cog-config/knowledge-base /Users/kevin/.hermes/knowledgebase
```

Verify:

```bash
python3 - <<'PY'
import os
for p in ['/Users/kevin/.claude/knowledgebase','/Users/kevin/.hermes/knowledgebase','/Users/kevin/projects/cog-config/knowledge-base']:
    print(p, 'exists=', os.path.exists(p), 'islink=', os.path.islink(p), 'real=', os.path.realpath(p) if os.path.exists(p) else '')
PY
```

## Ingest workflow

1. Load/read `/Users/kevin/.claude/skills/kb-add/SKILL.md`.
2. Get the URL or pasted article text from Kevin. If missing, ask for the URL/text.
3. For YouTube, use the `kb_add.py` script from the Claude skill; it can fetch transcripts.
4. For X/web articles, the Claude skill currently expects pasted content or a content file.
5. Let the script enforce:
   - author-first folder structure
   - double-underscore filename convention
   - required 11-field frontmatter
   - raw immutable source storage
6. Verify the created file exists and report the relative path.

## Important conventions from Claude kb-add

- KB root: `/Users/kevin/projects/cog-config/knowledge-base/`
- Structure: `{author-slug}/{original_date}__{format}__{title-slug}.md`
- Knowledge base is excluded from git and syncs through Google Drive.
- Do not summarize or overwrite raw source files unless Kevin explicitly asks.

## Search / index workflow

Use this when Kevin asks to find/search/list articles in the KB, e.g. “find me all the articles related to evals for LLMs.”

Primary search command:

```bash
~/.hermes/scripts/kb_search.py "QUERY" --limit 10
```

Index files maintained by the script:

```text
/Users/kevin/projects/cog-config/knowledge-base/.kb-index.sqlite
/Users/kevin/projects/cog-config/knowledge-base/INDEX.md
```

The script is intentionally more robust than grep:
- parses article frontmatter
- indexes title, author, tags, path, and full body with SQLite FTS5
- auto-refreshes when markdown files change
- expands common aliases like evals → evaluation/benchmark/judge/golden set
- requires clear multi-concept queries to match each concept when possible
- returns title, author/date, URL/path, and a matching snippet

After adding KB content, refresh the index:

```bash
~/.hermes/scripts/kb_search.py --rebuild --write-index
```

Claude-side companion skill exists at:

```text
/Users/kevin/.claude/skills/kb-search/SKILL.md
```

## Pitfalls

- Do not confuse this with Hermes `llm-wiki`, Obsidian, or `~/wiki`. Kevin's actual KB for this workflow is the Claude/cog-config knowledge base above.
- Do not ask Kevin to repeat the KB path; discover it first.
- If the user says "these articles" but no URLs/text came through, say the KB is ready and ask for the URLs/text.
- If updating more than a few existing files or changing schema conventions, ask before mass updates.
