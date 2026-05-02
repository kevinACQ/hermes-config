#!/usr/bin/env python3
"""Refresh Kevin's Hermes Claude Code project hub.

Scans ~/projects for git repos, creates/updates symlinks in the stable Hermes hub,
and regenerates PROJECTS.md. Safe by default: it only removes stale symlinks, not
real files or directories.
"""

import argparse
import configparser
from dataclasses import dataclass
from datetime import datetime
from pathlib import Path
from typing import Dict, List, Optional

DEFAULT_PROJECTS_ROOT = Path.home() / "projects"
DEFAULT_HUB_ROOT = Path.home() / ".hermes" / "workspace" / "claude-code-projects"
MANAGED_HEADER = "# Claude Code Project Hub for Hermes"


@dataclass(frozen=True)
class Project:
    name: str
    path: Path
    branch: str
    origin: str


def read_branch(repo: Path) -> str:
    head = repo / ".git" / "HEAD"
    if not head.exists():
        return "unknown"
    text = head.read_text(errors="ignore").strip()
    prefix = "ref: refs/heads/"
    if text.startswith(prefix):
        return text[len(prefix):]
    return text[:12] if text else "unknown"


def read_origin(repo: Path) -> str:
    config_path = repo / ".git" / "config"
    if not config_path.exists():
        return "(no origin)"
    parser = configparser.ConfigParser()
    try:
        parser.read(config_path)
        return parser.get('remote "origin"', "url", fallback="(no origin)")
    except configparser.Error:
        return "(no origin)"


def scan_projects(projects_root: Path) -> List[Project]:
    if not projects_root.exists():
        return []
    projects = []
    for child in sorted(projects_root.iterdir(), key=lambda p: p.name.lower()):
        if child.is_dir() and (child / ".git").exists():
            projects.append(
                Project(
                    name=child.name,
                    path=child.resolve(),
                    branch=read_branch(child),
                    origin=read_origin(child),
                )
            )
    return projects


def render_projects_md(projects: List[Project], projects_root: Path) -> str:
    generated = datetime.now().strftime("%Y-%m-%d %H:%M")
    lines = [
        MANAGED_HEADER,
        "",
        f"Generated: {generated}",
        "",
        "This folder gives Hermes one stable place to access projects Kevin builds in Claude Code.",
        "",
        "It is auto-refreshed from `~/projects` by `~/.hermes/scripts/refresh_claude_code_projects.py`.",
        "",
        "## Projects",
        "",
    ]
    if projects:
        for project in projects:
            lines.append(f"- [{project.name}](./{project.name}) — `{project.branch}` — `{project.origin}`")
    else:
        lines.append(f"No git repositories found in `{projects_root}`.")
    lines.extend([
        "",
        "## Rule",
        "",
        "Use the symlink path here for discovery, but remember the real repo lives in `~/projects/<name>`. Git operations work normally through either path.",
        "",
        "## Refresh command",
        "",
        "```bash",
        "python3 ~/.hermes/scripts/refresh_claude_code_projects.py",
        "```",
        "",
    ])
    return "\n".join(lines)


def refresh(projects_root: Path = DEFAULT_PROJECTS_ROOT, hub_root: Path = DEFAULT_HUB_ROOT) -> Dict[str, int]:
    projects_root = Path(projects_root).expanduser().resolve()
    hub_root = Path(hub_root).expanduser()
    hub_root.mkdir(parents=True, exist_ok=True)

    projects = scan_projects(projects_root)
    desired = {project.name: project.path for project in projects}

    added = 0
    removed = 0

    for entry in hub_root.iterdir():
        if entry.name in {"PROJECTS.md", "HERMES.md"}:
            continue
        if entry.is_symlink() and entry.name not in desired:
            entry.unlink()
            removed += 1

    for name, target in desired.items():
        link = hub_root / name
        if link.is_symlink():
            if link.resolve() != target:
                link.unlink()
                link.symlink_to(target, target_is_directory=True)
                added += 1
        elif not link.exists():
            link.symlink_to(target, target_is_directory=True)
            added += 1

    (hub_root / "PROJECTS.md").write_text(render_projects_md(projects, projects_root))

    hermes_md = hub_root / "HERMES.md"
    if not hermes_md.exists():
        hermes_md.write_text(
            "# Hermes Project Hub Context\n\n"
            "This directory is a symlink hub for Kevin's local Claude Code projects. "
            "Prefer this hub for discovery, then work inside the linked repo normally.\n"
        )

    return {"added": added, "removed": removed, "projects": len(projects)}


def main() -> int:
    parser = argparse.ArgumentParser(description="Refresh the Hermes Claude Code project hub.")
    parser.add_argument("--projects-root", type=Path, default=DEFAULT_PROJECTS_ROOT)
    parser.add_argument("--hub-root", type=Path, default=DEFAULT_HUB_ROOT)
    args = parser.parse_args()
    result = refresh(args.projects_root, args.hub_root)
    print(
        "Refreshed Claude Code project hub: "
        f"{result['projects']} projects, {result['added']} links added/updated, {result['removed']} stale links removed."
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
