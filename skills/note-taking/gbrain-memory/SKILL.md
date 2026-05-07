---
name: gbrain-memory
description: Use GBrain as Hermes's rich long-term memory layer for durable project context, decisions, workflows, people, companies, and memory-heavy recall questions.
version: 1.0.0
author: Hermes Agent
license: MIT
metadata:
  hermes:
    tags: [memory, gbrain, mcp, knowledge-base]
---

# GBrain Memory

Use this skill when Kevin asks about memory-heavy context, including:

- “remember”, “what did we decide”, “what do you know about”, “last time”, “across tools”, “memory”, “brain”
- Durable preferences, people, companies, projects, decisions, workflows, or cross-tool knowledge
- High-stakes recommendations where prior context could materially change the answer

## Architecture

Hermes has three complementary memory surfaces:

| Information type | Destination |
|---|---|
| Must influence every Hermes turn | Hermes `memory` / user profile |
| Rich project history and decisions | GBrain |
| Raw transcript/session recall | Hermes `session_search` |
| Procedures/workflows | Hermes skills, indexed in GBrain when useful |
| Temporary TODO state | Current session TODO only |
| Secrets/API keys | Nowhere in memory |

## How to use GBrain

Preferred live integration is the native MCP server configured as `gbrain`:

- Wrapper: `/Users/kevin/.hermes/scripts/gbrain-mcp.sh`
- Brain markdown repo: `/Users/kevin/.hermes/brain`
- GBrain home: `/Users/kevin/.hermes`
- DB/config: `/Users/kevin/.hermes/.gbrain`

MCP tools are named with the `mcp_gbrain_` prefix after Hermes startup, for example:

- `mcp_gbrain_search`
- `mcp_gbrain_query`
- `mcp_gbrain_get_page`
- `mcp_gbrain_put_page`
- `mcp_gbrain_list_pages`
- `mcp_gbrain_get_stats`

If MCP tools are unavailable in the current process, use the CLI fallback:

```bash
export PATH="$HOME/.bun/bin:$PATH"
export GBRAIN_HOME=/Users/kevin/.hermes
cd /Users/kevin/.hermes/brain
gbrain search "query terms"
gbrain query "natural-language question"
gbrain stats
```

## Operating procedure

1. Search GBrain first for durable memory context.
2. Use Hermes `session_search` second if the question references past chats or details not yet consolidated into GBrain.
3. Answer with provenance:
   - User said
   - GBrain says
   - Hermes session history says
   - Inference
4. Write back stable new facts to GBrain when they are durable and useful.
5. Use Hermes `memory` only for compact facts that should be injected every turn.

## Write-back rules

Write to GBrain when:

- Kevin makes a durable decision
- A project architecture or workflow changes
- A stable preference/person/company/project fact is discovered
- A session summary is worth preserving beyond raw transcript search

Do not write:

- Raw secrets or credentials
- Temporary task progress
- Raw full transcripts unless Kevin explicitly asks
- Low-confidence inferences without labeling them

## Verification

A healthy integration should pass:

```bash
hermes mcp test gbrain
GBRAIN_HOME=/Users/kevin/.hermes gbrain stats
GBRAIN_HOME=/Users/kevin/.hermes gbrain search "Kevin working style"
```

The integration is only genuinely improving Hermes memory if Hermes can retrieve GBrain-only content and use it in an answer.
