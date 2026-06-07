---
name: external-skill-library-migration
description: Use when importing, mirroring, or making another agent's SKILL.md library available to Hermes without losing the original source of truth. Covers Claude Code, gstack, plugin skill trees, symlink mirrors, skills.external_dirs, conflict handling, verification, and backup.
version: 1.0.0
author: Hermes Agent
license: MIT
metadata:
  hermes:
    tags: [skills, migration, claude-code, external-dirs, symlinks, hermes-agent]
    related_skills: [hermes-agent-skill-authoring, hermes-agent]
---

# External Skill Library Migration

## Overview

Use this skill when the user wants skills from another agent environment to work in Hermes while preserving the original library exactly as designed.

The default recommendation is **do not copy the skills**. Create a Hermes-readable mirror made of symlinks and register that mirror through `skills.external_dirs`. This keeps one source of truth, avoids drift, and lets Hermes load the same `SKILL.md` files directly.

This is especially useful for Claude Code skill libraries under `~/.claude/skills`, gstack skill packs, and other `SKILL.md`-based agent workflows.

## When to Use

Use when the user asks to:

- import Claude Code skills into Hermes
- make another agent's skills visible to Hermes
- preserve skills “exactly as designed”
- investigate existing skill symlinks or skill folders
- migrate a skill library without duplicating files
- debug why Hermes cannot see skills from another directory

Do **not** use for:

- writing a brand-new single skill from scratch; use `hermes-agent-skill-authoring`
- installing public hub skills with `hermes skills install`
- editing bundled/protected Hermes skills directly

## Recommended Architecture

### Source of truth

Keep the original skill library as source of truth, for example:

```text
~/.claude/skills
```

### Hermes mirror

Create a mirror directory under Hermes external repos:

```text
~/.hermes/external-repos/<source>-skills
```

Each child in the mirror should usually be a symlink to one source skill directory:

```text
~/.hermes/external-repos/claude-code-skills/prototype-first -> ~/.claude/skills/prototype-first
```

### Hermes config

Register the mirror through `skills.external_dirs` in `~/.hermes/config.yaml`:

```yaml
skills:
  external_dirs:
    - /Users/kevin/.hermes/external-repos/claude-code-skills
```

Hermes scans `~/.hermes/skills` first, then `skills.external_dirs`. Local Hermes skills take precedence.

## Migration Workflow

1. **Find candidate source folders**
   - Check the expected source first, usually `~/.claude/skills`.
   - Look for directories containing `SKILL.md`.
   - Avoid dependency and generated trees like `node_modules`, `.git`, `.venv`, `venv`, cache folders, and hidden generated agent directories unless the user explicitly wants them.

2. **Check existing symlinks**
   - Inspect both source and Hermes paths.
   - Distinguish knowledge-base symlinks from skill-library symlinks. A shared `knowledgebase` symlink does not mean skills are already shared.

3. **Detect name collisions before linking**
   - Parse each candidate's frontmatter `name` field.
   - Compare against existing Hermes skill names.
   - Also detect duplicate names inside the external source library.
   - Do not blindly expose duplicates; Hermes `skill_view` refuses ambiguous bare names.

4. **Create a symlink mirror**
   - Link only selected, non-conflicting skill directories.
   - Prefer stable, class-level skill dirs over archived, generated, dependency, or hidden copies.
   - If the same skill appears in a top-level source directory and inside a generated pack, prefer the top-level/user-facing source.

5. **Write a manifest**
   - Include source root.
   - List linked skills and skipped conflicts.
   - Explain that source edits happen in the original library and Hermes sees them through symlinks after reload/new session.

6. **Register `skills.external_dirs`**
   - Add the mirror path, preserving any existing external dirs.
   - Do not replace unrelated skill config.

7. **Verify**
   - Run `hermes skills list` or use `skills_list` in-session.
   - Load representative migrated skills with `skill_view`.
   - Verify one simple skill, one skill with scripts/references, and one nested pack skill if present.

8. **Back up config**
   - If the user has a Hermes config backup repo, sync and commit the config change.
   - Commit the config change, not the symlink mirror target contents, unless the repo is explicitly intended to track them.

## Collision Policy

A collision is not a failure. It is a routing decision.

Default policy:

- Existing Hermes skill wins for duplicate names.
- User-facing top-level source skill wins over generated/internal copies.
- Skipped conflicts go into the manifest.
- Do not rename a skill unless the user explicitly wants both variants callable by bare name.

Common conflicts:

- `humanizer` may already exist in Hermes and in Claude.
- `codex` may already exist in Hermes and in Claude/gstack.
- gstack may contain many generated variants across `.cursor`, `.opencode`, `.agents`, `.factory`, `.hermes`, etc. Do not expose all of them by default.

## Verification Checklist

- [ ] Source skill root identified.
- [ ] Existing symlinks checked; no assumption that knowledge-base links imply skill links.
- [ ] Mirror directory created under `~/.hermes/external-repos/`.
- [ ] Mirror entries are symlinks, not copies, unless copying was explicitly requested.
- [ ] Duplicate skill names detected and skipped or explicitly resolved.
- [ ] Manifest lists linked and skipped skills.
- [ ] `skills.external_dirs` includes the mirror path.
- [ ] `hermes skills list` or `skills_list` shows representative imported skills.
- [ ] `skill_view` works on at least 2-3 representative imported skills.
- [ ] Config backup committed if the user has a config backup repo.

## Common Pitfalls

1. **Copying instead of symlinking.** Copying creates drift. If the user says “exactly how I designed them,” preserve the original files and symlink them.

2. **Exposing generated duplicates.** Some skill packs contain generated variants for multiple agents. Registering all of them creates name collisions and noisy skill lists.

3. **Assuming a symlink already exists.** Verify with filesystem inspection. Knowledge-base symlinks and skill-library symlinks are separate.

4. **Creating ambiguous bare names.** Hermes intentionally refuses to guess when multiple `SKILL.md` files have the same name. Detect and handle conflicts first.

5. **Forgetting session reload behavior.** New skills may require a new Hermes session or `/reload-skills` before they appear in the prompt context.

6. **Editing protected bundled skills to record a migration.** If the lesson is about migration mechanics, create or update a user-local umbrella skill instead of patching bundled skills.

## Reference Files

- `references/claude-code-skills-to-hermes.md` — concrete recipe and session-derived notes for mirroring Claude Code skills into Hermes.
