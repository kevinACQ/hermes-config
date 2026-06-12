---
name: github-workflows
description: "Use when working with GitHub end-to-end: authentication, repository management, issue triage, PR creation/review/merge, CI checks, releases, and codebase inspection."
version: 1.0.0
author: Hermes Agent
license: MIT
platforms: [linux, macos, windows]
metadata:
  hermes:
    tags: [github, git, gh, pull-requests, issues, code-review, repositories, ci]
    related_skills: [requesting-code-review, systematic-debugging]
---

# GitHub Workflows

## Overview

Class-level umbrella for GitHub work. It replaces narrow skills for auth setup, repo management, issue operations, PR lifecycle, PR review, and codebase inspection. Use it to choose the right GitHub route (`git`, `gh`, or REST/GraphQL), perform prerequisite checks, and verify side effects.

## When to Use

- Clone/fork/create repositories; inspect remotes, branches, releases, or repo settings.
- Authenticate `gh`, SSH, or HTTPS tokens.
- Create, triage, label, assign, or close issues.
- Create branches, commits, PRs, run CI checks, merge/land changes.
- Review pull requests or diffs before landing.
- Inspect a codebase's languages/LOC/composition.

## Prerequisite Checks

1. `git status --short --branch` to understand workspace state.
2. `gh auth status` when GitHub API access is needed.
3. `git remote -v` and `gh repo view --json nameWithOwner,defaultBranchRef` to identify the target repo.
4. For PRs, identify base/head branches and whether CI is required.
5. For destructive operations (delete branch, close issue, merge), confirm scope and verify permissions.

## Authentication

- Prefer `gh auth login`/`gh auth status` for REST/GraphQL operations.
- Use SSH keys for git remotes when the repo already uses SSH.
- Do not paste or print tokens. If auth is missing, guide the user through `gh auth login` or credential setup.

## Repository Management

- Use `gh repo clone`, `gh repo create`, `gh repo fork`, `git remote`, and release commands.
- Always verify the resulting repository path/remote URL.
- For releases, inspect tags and existing releases before creating or replacing anything.

## Issues

- Search for existing issues before creating duplicates.
- Use templates when present (`.github/ISSUE_TEMPLATE`).
- Include reproduction, expected behavior, actual behavior, environment, and acceptance criteria.
- For triage, labels/assignees should match repo conventions; inspect existing labels first.

## Pull Requests

- Branch from the correct base; keep branch names descriptive.
- Before opening: run the relevant tests/lints, inspect `git diff`, and ensure no secrets or unrelated files are included.
- PR body should include summary, tests run, risk/rollback notes, and linked issues when applicable.
- After opening, monitor CI with `gh pr checks` or `gh run watch` and fix failures rather than reporting success prematurely.

## Code Review

- Review the diff against the intended base, not just changed files in isolation.
- Prioritize correctness, security, data loss, race conditions, migration safety, and test coverage.
- Provide actionable comments with file/line references when possible.
- Distinguish blockers from nits.

## Codebase Inspection

- Use LOC/language tools such as `pygount` only after excluding generated/vendor/build directories.
- Report ratios and notable hotspots, not just raw line counts.

## Verification Checklist

- [ ] Auth and target repo verified.
- [ ] Current branch/worktree state understood.
- [ ] Side effects (issues, PRs, releases, merges) confirmed by `gh` output/URL.
- [ ] Tests/checks actually run when code changed.
- [ ] Final response includes URLs/IDs for created GitHub artifacts.

## Consolidated Legacy Skills

Absorbed: `github-auth`, `github-repo-management`, `github-issues`, `github-pr-workflow`, `github-code-review`, and `codebase-inspection`. Archived packages retain detailed templates/scripts; promote any recurring repo-specific recipe back into this umbrella as a reference file.
