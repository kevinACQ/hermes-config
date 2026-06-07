#!/usr/bin/env python3
"""Refresh Hermes's token-efficient mirror of Kevin's Claude Code skills.

Design:
- Claude remains source of truth: ~/.claude/skills
- Hermes gets symlink entries under ~/.hermes/external-repos/claude-code-skills
- Mirrored skills are disabled by default so they do NOT bloat Hermes's system prompt
- A single enabled Hermes index skill explains how to load them explicitly
- Known Claude-memory writers are excluded so Hermes does not write into ~/.claude/memory
"""
from __future__ import annotations

import os
import re
from pathlib import Path
from typing import Iterable

import yaml

CLAUDE_SKILLS = Path.home() / ".claude" / "skills"
MIRROR = Path.home() / ".hermes" / "external-repos" / "claude-code-skills"
HERMES_SKILLS = Path.home() / ".hermes" / "skills"
HERMES_CONFIG = Path.home() / ".hermes" / "config.yaml"

# These are Claude architecture / memory lifecycle skills. Hermes must not run
# them against ~/.claude. Hermes-native replacements should live in ~/.hermes/skills.
EXCLUDE_NAMES = {
    "session-close",
    "remember-fact",
    "state-transfer",
}

# Hermes-native skills win. Do not create ambiguous duplicates.
HERMES_NATIVE_PREFERRED = {
    "codex",
    "humanizer",
}

# Ignore generated/agent-specific vendor trees inside gstack and dependencies.
EXCLUDED_PARTS = {
    ".git", ".github", ".cursor", ".gbrain", ".opencode", ".agents",
    ".openclaw", ".slate", ".factory", ".kiro", ".hermes", "node_modules",
    "venv", ".venv", "__pycache__",
}


def parse_name(skill_md: Path) -> str:
    text = skill_md.read_text(errors="ignore")[:1600]
    m = re.search(r"^name:\s*[\"']?([^\"'\n]+)", text, re.M)
    return (m.group(1).strip() if m else skill_md.parent.name)[:64]


def hermes_native_names() -> set[str]:
    names = set()
    for md in HERMES_SKILLS.rglob("SKILL.md"):
        if any(part in {".archive", ".git", "node_modules", "venv", ".venv"} for part in md.parts):
            continue
        names.add(parse_name(md))
    return names


def candidate_skill_dirs() -> Iterable[Path]:
    # Main user-created Claude skills.
    for child in sorted(CLAUDE_SKILLS.iterdir()):
        if child.is_dir() and not child.name.startswith(".") and (child / "SKILL.md").exists():
            yield child

    # Active gstack skill pack, immediate children only.
    gstack = CLAUDE_SKILLS / "gstack"
    if gstack.exists():
        for child in sorted(gstack.iterdir()):
            if child.is_dir() and not child.name.startswith(".") and (child / "SKILL.md").exists():
                yield child

    # OpenClaw gstack extras, immediate children only.
    openclaw = gstack / "openclaw" / "skills"
    if openclaw.exists():
        for child in sorted(openclaw.iterdir()):
            if child.is_dir() and not child.name.startswith(".") and (child / "SKILL.md").exists():
                yield child


def refresh() -> None:
    MIRROR.mkdir(parents=True, exist_ok=True)

    # Remove old symlinks and manifest. Never delete real directories.
    for child in list(MIRROR.iterdir()):
        if child.is_symlink() or child.name == "MANIFEST.md":
            child.unlink()

    native = hermes_native_names()
    seen: set[str] = set()
    linked: list[tuple[str, Path]] = []
    skipped: list[tuple[str, Path, str]] = []

    for skill_dir in candidate_skill_dirs():
        if any(part in EXCLUDED_PARTS for part in skill_dir.parts):
            continue
        name = parse_name(skill_dir / "SKILL.md")
        reason = None
        if name in EXCLUDE_NAMES:
            reason = "excluded: Claude memory/session architecture writer"
        elif name in seen:
            reason = "duplicate within Claude active set"
        elif name in HERMES_NATIVE_PREFERRED and name in native:
            reason = "Hermes-native skill preferred"
        elif name in native:
            reason = "duplicate with existing Hermes skill"

        if reason:
            skipped.append((name, skill_dir, reason))
            continue

        seen.add(name)
        link = MIRROR / name
        link.symlink_to(skill_dir, target_is_directory=True)
        linked.append((name, skill_dir))

    manifest = [
        "# Claude Code skills mirror for Hermes",
        "",
        f"Source: `{CLAUDE_SKILLS}`",
        "",
        "This directory contains symlinks only. Claude remains the source of truth.",
        "Hermes disables these mirrored skills by default to avoid hidden token burn; load them explicitly when needed.",
        "Claude memory/session-writing skills are intentionally excluded so Hermes does not write into ~/.claude.",
        "",
        "## Linked skills",
    ]
    manifest += [f"- `{name}` → `{path}`" for name, path in sorted(linked)]
    manifest += ["", "## Skipped"]
    manifest += [f"- `{name}` → `{path}` ({reason})" for name, path, reason in sorted(skipped)]
    (MIRROR / "MANIFEST.md").write_text("\n".join(manifest) + "\n", encoding="utf-8")

    cfg = yaml.safe_load(HERMES_CONFIG.read_text()) or {}
    skills = cfg.setdefault("skills", {})
    external = skills.get("external_dirs") or []
    if isinstance(external, str):
        external = [external]
    mirror_s = str(MIRROR)
    if mirror_s not in external:
        external.append(mirror_s)
    skills["external_dirs"] = external

    disabled = set(skills.get("disabled") or [])
    # Disable all mirrored Claude skills by default. Explicit skill_view still works,
    # but they won't appear in the always-on prompt skill catalog.
    disabled.update(name for name, _ in linked)
    disabled.update(HERMES_NATIVE_PREFERRED)  # humanizer/codex ambiguity control; codex can be re-enabled if desired.
    disabled.discard("session-close")  # Hermes-native safe close stays available.
    skills["disabled"] = sorted(disabled)

    HERMES_CONFIG.write_text(yaml.safe_dump(cfg, sort_keys=False, allow_unicode=True), encoding="utf-8")

    print(f"linked={len(linked)} skipped={len(skipped)} mirror={MIRROR}")


if __name__ == "__main__":
    refresh()
