---
name: ai-coding-agents
description: "Use when delegating implementation, review, or repository work to external AI coding CLIs such as Claude Code, Codex, OpenCode, or Hermes subprocesses."
version: 1.0.0
author: Hermes Agent
license: MIT
platforms: [linux, macos, windows]
metadata:
  hermes:
    tags: [ai-agents, claude-code, codex, opencode, delegation, coding]
    related_skills: [github-workflows, systematic-debugging, test-driven-development]
---

# AI Coding Agents

## Overview

Use this class-level skill when spawning or delegating to autonomous coding agents. Provider-specific CLIs differ, but the operating model is the same: define the task boundary, isolate the workspace, give exact verification requirements, monitor output, and verify artifacts yourself before claiming success.

## When to Use

- User explicitly asks to use Claude Code, Codex, OpenCode, or another coding agent.
- Work can be split into independent implementation/review/research streams.
- A long-running agent process is useful because the task exceeds normal subagent scope.
- You need an external ACP-compatible CLI or terminal-based coding assistant.

Do not use when a direct file edit/test loop is faster, or when the task needs real-time user clarification inside the child process.

## Agent Choice

| Agent | Best for | Notes |
|---|---|---|
| Claude Code | Large repo edits, long implementation, PR polishing | Strong autonomous coding; monitor for over-broad edits. |
| Codex | OpenAI Codex CLI coding/review flows | Good for focused patches; pass exact constraints. |
| OpenCode | Alternative coding/review CLI | Useful when configured locally or preferred by user. |
| Hermes subprocess | Full Hermes tools/session isolation | Use for durable missions or interactive tmux sessions. |
| `delegate_task` | Synchronous bounded subtask | Parent waits; child is cancelled if parent is interrupted. |

## Standard Delegation Contract

Every spawned coding agent prompt should include:

1. Goal and non-goals.
2. Repo path and branch/worktree constraints.
3. Exact files/areas allowed or forbidden.
4. Required tests/commands and expected evidence.
5. Output contract: summary, files changed, commands run, blockers, URLs/IDs.
6. Instruction not to claim success without real verification output.

## Workspace Isolation

- Prefer git worktrees or isolated branches for parallel agents.
- Snapshot `git status --short --branch` before and after.
- Do not let multiple agents edit the same files unless orchestrated through a board/queue.
- Before merging agent output, inspect diffs yourself.

## Running CLIs

- Use PTY/tmux for interactive terminal agents.
- Use foreground commands for short one-shot runs; background with `notify_on_complete=true` for bounded long runs.
- Do not pass secrets into prompts. Use existing environment/config when required.

## Verification

Subagent self-reports are not proof. Verify by reading changed files, running tests, checking `git diff`, and fetching URLs/PRs returned by the agent.

## Common Pitfalls

- Vague prompts produce sweeping rewrites.
- Letting agents share a dirty worktree causes hidden conflicts.
- Trusting "tests passed" without real output leads to false completion.
- Forgetting to constrain formatting/docs causes churn.

## Consolidated Legacy Skills

Absorbed provider-specific skills: `claude-code`, `codex`, and `opencode`. Provider quirks should live as subsections or references here rather than standalone micro-skills.
