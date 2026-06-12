---
name: kanban-workflows
description: "Use when coordinating Hermes Kanban boards, orchestrator profiles, and worker profiles for durable multi-agent work queues."
version: 1.0.0
author: Hermes Agent
license: MIT
platforms: [linux, macos, windows]
metadata:
  hermes:
    tags: [kanban, orchestration, workers, multi-agent, queues]
    related_skills: [ai-coding-agents, hermes-agent]
---

# Kanban Workflows

## Overview

Umbrella for Hermes Kanban usage: orchestrators decompose and route work; workers execute narrowly-scoped tasks and report state through the board. The board is the durable coordination boundary.

## When to Use

- User asks to coordinate multiple agents or profiles through a durable queue.
- Work needs assignment, dependencies, comments, retries, or handoffs.
- A worker profile is spawned by the dispatcher and must follow Kanban tool boundaries.
- You need to inspect or repair a board's task state.

## Roles

### Orchestrator

- Break goals into small tasks with clear acceptance criteria.
- Assign profiles intentionally; do not do worker work directly if the goal is queue orchestration.
- Link dependencies and unblock only when prerequisites are truly satisfied.
- Monitor stale/failed tasks and adjust scope rather than repeatedly respawning doomed work.

### Worker

- Read the assigned task, constraints, and linked context first.
- Work only on the task boundary; ask/flag blockers through Kanban comments.
- Heartbeat during long work.
- Complete only after verification evidence exists.

## Board Lifecycle

1. Initialize/select the board and tenant/workspace.
2. Create tasks with explicit done criteria.
3. Link dependencies.
4. Assign profiles.
5. Dispatcher claims and spawns workers.
6. Workers comment, block, heartbeat, or complete.
7. Orchestrator reviews output and closes the loop.

## Anti-Temptation Rules

- Orchestrators should not silently perform worker implementation just because they can.
- Workers should not create broad follow-up tasks to escape their assigned scope unless there is a real blocker.
- Do not mark complete based only on intent; require evidence.

## Consolidated Legacy Skills

Absorbed `kanban-orchestrator` and `kanban-worker`. Keep role-specific details as labeled sections in this umbrella.
