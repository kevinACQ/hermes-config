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

Explicit raw-transcript exception:

- If Kevin explicitly asks for Retell/Hermes Voice calls to be remembered word-for-word, store transcripts in the raw layer under `~/.hermes/brain/raw/retell-calls/` and create linked structured session pages under `~/.hermes/brain/sessions/retell/`. Keep extracted durable memories separate and approval-gated; the transcript archive is evidence, not automatically compiled memory.

## No-API-key GBrain setup

Use this when Kevin asks how to make GBrain work without API keys or with OAuth-only resources.

Key findings from Kevin's setup:

- GBrain v0.27 supports pluggable embedding providers.
- Claude OAuth and ChatGPT OAuth are useful at the Hermes/agent reasoning layer, but GBrain does not consume those OAuth sessions directly for embeddings.
- Anthropic does not provide a first-party embedding model in GBrain; an Anthropic API key can help expansion/chat/subagents, but not core vector embeddings.
- Gemini embeddings require `GOOGLE_GENERATIVE_AI_API_KEY`; a Google Workspace/Gemini account alone is not enough for GBrain's native Gemini embedding path.
- The clean no-API-key path is local Ollama embeddings.

Recommended no-key architecture:

```text
Hermes reasoning:     Claude OAuth / ChatGPT OAuth
GBrain database:      local PGLite
GBrain embeddings:   local Ollama + nomic-embed-text
GBrain expansion:    skip, or optional Anthropic API key
```

Discovery commands:

```bash
export PATH="$HOME/.local/bin:$HOME/.bun/bin:$PATH"
export GBRAIN_HOME=/Users/kevin/.hermes
gbrain providers list
gbrain providers explain --json
gbrain config show
command -v ollama || true
pgrep -af '[o]llama' || true
test -d "$HOME/Applications/Ollama.app" && echo "$HOME/Applications/Ollama.app exists" || true
test -d /Applications/Ollama.app && echo "/Applications/Ollama.app exists" || true
curl -sS --max-time 3 http://127.0.0.1:11434/api/version || true
ollama list 2>&1 || true
```

Kevin's no-admin Mac setup can still have Ollama working without `/Applications/Ollama.app`: the app may live at `~/Applications/Ollama.app`, with the CLI symlink at `~/.local/bin/ollama`, serving on `localhost:11434`. Do not infer Ollama is missing just because moving it to `/Applications` asked for an admin password; verify the user-space install and local API first.

Setup once Ollama is installed/running:

```bash
ollama serve
ollama pull nomic-embed-text
export PATH="$HOME/.bun/bin:$PATH"
export GBRAIN_HOME=/Users/kevin/.hermes
gbrain config set embedding_model ollama:nomic-embed-text
gbrain config set embedding_dimensions 768
gbrain embed --stale
```

Verify:

```bash
GBRAIN_HOME=/Users/kevin/.hermes gbrain providers list
GBRAIN_HOME=/Users/kevin/.hermes gbrain health
GBRAIN_HOME=/Users/kevin/.hermes gbrain query "Kevin working style"
```

If Ollama is not installed, report that as the single blocker. Do not suggest OAuth-browser-session hacks unless Kevin explicitly wants to build/maintain a custom adapter; they are fragile and outside GBrain's supported provider path.

## Evaluating GBrain embedding quality and model tradeoffs

Use this when Kevin asks whether Ollama embeddings are good enough, or asks to compare Ollama with GPT/Claude/API-key options for GBrain.

Key framing:

- For GBrain, distinguish **embedding/retrieval** from **reasoning/answer synthesis**.
- Ollama `nomic-embed-text` is the current local embedding provider. GPT-5.5 and Claude Opus-style models are mainly reasoning models; they can synthesize retrieved memory but do not directly improve vector retrieval unless GBrain is configured with a stronger embedding provider.
- Anthropic/Claude does not provide the core first-party embedding replacement in GBrain; an Anthropic key can help expansion/chat/reasoning, not the vector store itself.
- Generic LLM benchmarks are less relevant than retrieval benchmarks and Kevin-specific recall tests.

Relevant benchmark lenses for Kevin's use case:

1. Retrieval accuracy — does the right memory page appear?
2. Ranking quality — does the most specific page rank above generic pages like `people/kevin`?
3. Recall under vague prompts — can GBrain find decisions when Kevin asks imprecisely?
4. Latency — local Ollama vs cloud round trips.
5. Privacy — local memory chunks vs provider upload.
6. Operational reliability — local Ollama availability vs cloud API/rate-limit/key/billing dependencies.

Live trace pattern to show real quality:

```bash
export PATH="$HOME/.local/bin:$HOME/.bun/bin:$PATH"
export GBRAIN_HOME=/Users/kevin/.hermes
cd /Users/kevin/.hermes/brain
printf '## CONFIG\n'; gbrain config show
printf '\n## HEALTH\n'; gbrain health
printf '\n## QUERY: Kevin working style\n'; gbrain query "Kevin working style" --limit 5
printf '\n## QUERY: Retell voice onboarding memory\n'; gbrain query "Retell voice onboarding memory" --limit 5
```

Interpretation guidance:

- If specific pages appear in top 3, Ollama is probably good enough.
- If generic pages repeatedly outrank obvious specific pages, consider an embedding A/B test before switching providers.
- For free/local alternatives, test `bge-m3` or `mxbai-embed-large` against `nomic-embed-text` on Kevin-specific queries. Do not switch blindly because dimension changes may require rebuilding/re-embedding the GBrain DB.
- For paid upgrades, prefer a real embedding provider such as OpenAI embeddings or Voyage-style embeddings over reasoning models if the bottleneck is recall/ranking.

Recommended A/B test workflow:

1. Create 15-25 real Kevin queries covering preferences, GBrain setup, Retell voice memory, Claude project hub, config backup, and decisions.
2. For each candidate embedding model, rebuild or use an isolated temporary GBrain DB with that model/dimension.
3. Run `gbrain query "$QUERY" --limit 5` for each query.
4. Score top-1, top-3, and top-5 hit rate, plus whether specific pages outrank generic pages.
5. Switch only if the candidate materially improves top-3 specificity without unacceptable latency/setup cost.

## Maintenance pass workflow

Use this when asked to run local GBrain sync/embed maintenance, especially from a cron job where no user is present.

1. Run the requested CLI commands with Kevin's environment:

```bash
export PATH="$HOME/.bun/bin:$PATH"
export GBRAIN_HOME=/Users/kevin/.hermes
cd /Users/kevin/.hermes/brain
gbrain sync --repo /Users/kevin/.hermes/brain
gbrain embed --stale
```

2. If `gbrain sync` fails with the known PGLite WASM runtime issue, do not treat GBrain as unavailable. Try MCP fallback:

```text
mcp_gbrain_sync_brain(repo="/Users/kevin/.hermes/brain", no_embed=true)
```

Report MCP `up_to_date` as a successful sync fallback.

3. If `gbrain embed --stale` fails:
   - If the error is missing API key/provider/embedding provider, report it as a warning, not fatal; keyword search still works.
   - If the error is the PGLite WASM runtime issue, report embeddings as blocked by local GBrain/PGLite runtime.
   - Optionally submit an MCP `embed` job only if a worker appears available. If the job remains `waiting` after a short check and no worker is active, cancel it to avoid queue clutter.

4. Verify with MCP stats/health when available:

```text
mcp_gbrain_get_stats()
mcp_gbrain_get_health()
```

5. Final cron reports should be concise: status, warnings, and needed action. Do not schedule additional cron jobs from inside cron-run sessions.

## Verification

A healthy integration should pass:

```bash
hermes mcp test gbrain
GBRAIN_HOME=/Users/kevin/.hermes gbrain stats
GBRAIN_HOME=/Users/kevin/.hermes gbrain health
GBRAIN_HOME=/Users/kevin/.hermes gbrain search "Kevin working style"
```

Kevin's reusable smoke-test script is:

```bash
/Users/kevin/.hermes/scripts/verify-gbrain-hermes.sh
```

This script checks GBrain version, doctor, stats, health, search, query, `hermes mcp list`, and `hermes mcp test gbrain`.

The integration is only genuinely improving Hermes memory if Hermes can retrieve GBrain-only content and use it in an answer.

If native `mcp_gbrain_*` tools in the currently running Hermes session return `ClosedResourceError` but `hermes mcp test gbrain` passes, treat the current session's MCP client as stale rather than treating GBrain as broken. Use CLI fallback for the current task, and refresh the Hermes session/gateway before relying on native MCP tools in that same process.

## Full implementation / seeding workflow

Use this when executing a broad GBrain integration plan or recovering from a partially completed setup.

1. Verify the live baseline first:

```bash
export PATH="$HOME/.local/bin:$HOME/.bun/bin:$PATH"
export GBRAIN_HOME=/Users/kevin/.hermes
gbrain --version
cd /Users/kevin/.hermes/brain
gbrain doctor --json
gbrain stats
gbrain health
hermes mcp list
hermes mcp test gbrain
```

2. If native MCP tools fail in-session, continue with the CLI if fresh `hermes mcp test gbrain` passes. Do not block the task on the stale tool client.

3. Seed durable memory as concise markdown pages, not raw transcripts. Good initial targets:

```text
/Users/kevin/.hermes/brain/sessions/hermes-config-backup.md
/Users/kevin/.hermes/brain/sessions/claude-code-project-hub.md
/Users/kevin/.hermes/brain/sessions/voice-onboarding-architecture.md
/Users/kevin/.hermes/brain/sessions/gbrain-integration-progress.md
```

Use `session_search` summaries as provenance, and include wiki links to existing pages such as `[[tools/gbrain]]`, `[[projects/hermes-agent]]`, and `[[workflows/gbrain-memory-routing]]`.

4. Import, embed, and backfill graph/timeline:

```bash
export PATH="$HOME/.local/bin:$HOME/.bun/bin:$PATH"
export GBRAIN_HOME=/Users/kevin/.hermes
cd /Users/kevin/.hermes/brain
gbrain import /Users/kevin/.hermes/brain --no-embed
gbrain embed --stale
gbrain extract links --source db
gbrain extract timeline --source db
gbrain stats
gbrain health
```

5. Commit local brain markdown changes so the private local brain has rollback history:

```bash
git -C /Users/kevin/.hermes/brain add -A
git -C /Users/kevin/.hermes/brain commit -m "chore: seed GBrain Hermes memory pages"
```

6. Re-run `/Users/kevin/.hermes/scripts/verify-gbrain-hermes.sh` and report only the high-level status, warnings, and remaining blocker.

## Known pitfall: PGLite CLI/MCP failure after half-migrated DB

On Kevin's macOS setup, direct `gbrain` CLI commands can fail with a PGLite WASM runtime error. This can look like a macOS/PGLite runtime bug, but on 2026-05-08 the root cause was the existing local PGLite DB being half-migrated/corrupted; a fresh temp PGLite brain worked.

Symptom:

```text
PGLite failed to initialize its WASM runtime.
This is most commonly the macOS 26.3 WASM bug
Original error: Aborted(). Build with -sASSERTIONS for more info.
```

Debug flow:

1. Test whether PGLite itself works with a temp brain:

```bash
export PATH="$HOME/.bun/bin:$PATH"
tmp=$(mktemp -d /tmp/gbrain-test.XXXXXX)
GBRAIN_HOME="$tmp" gbrain init --pglite
GBRAIN_HOME="$tmp" gbrain stats
```

2. If temp PGLite works but Kevin's DB fails, backup and rebuild from markdown:

```bash
export PATH="$HOME/.bun/bin:$PATH"
export GBRAIN_HOME=/Users/kevin/.hermes
cd /Users/kevin/.hermes/brain
cp -R ~/.hermes/.gbrain/brain.pglite ~/.hermes/.gbrain/brain.pglite.backup-$(date +%Y%m%d-%H%M%S)
mv ~/.hermes/.gbrain/brain.pglite ~/.hermes/.gbrain/brain.pglite.broken-$(date +%Y%m%d-%H%M%S)
gbrain init --pglite
gbrain import /Users/kevin/.hermes/brain --no-embed
gbrain apply-migrations --yes --non-interactive
gbrain stats
hermes mcp test gbrain
```

3. If `gbrain doctor` reports `MINIONS HALF-INSTALLED`, run:

```bash
gbrain apply-migrations --yes --non-interactive
```

4. PGLite does not use a persistent `jobs work` daemon. Use inline execution / `--follow`; don't submit MCP background jobs unless a worker is actually active. Cancel diagnostic jobs that remain `waiting`.

4a. If `gbrain health`, `gbrain stats`, or `hermes mcp test gbrain` fails with `Timed out waiting for PGLite lock`, inspect the lock file and live processes before rebuilding anything:

```bash
python3 -m json.tool /Users/kevin/.hermes/.gbrain/brain.pglite/.gbrain-lock/lock
ps -p <pid-from-lock> -o pid,ppid,stat,etime,command
ps aux | egrep 'gbrain|PGlite|bun|hermes' | egrep -v 'egrep|ps aux'
```

Observed cause on 2026-05-09: stale `gbrain serve` held the PGLite lock after MCP testing, blocking health/stats/MCP startup. Fix only after confirming the PID/command: stop the stale `gbrain serve` process, verify it exited, then remove only the stale `.gbrain-lock` directory if it remains. Re-verify with:

```bash
GBRAIN_HOME=/Users/kevin/.hermes gbrain health
hermes mcp test gbrain
```

5. For Kevin's current no-admin/no-API-key setup, embeddings should use Ollama:

```bash
export PATH="$HOME/.local/bin:$HOME/.bun/bin:$PATH"
export GBRAIN_HOME=/Users/kevin/.hermes
gbrain init --pglite --embedding-model ollama:nomic-embed-text --embedding-dimensions 768
# If rebuilding, import markdown and then embed:
gbrain import /Users/kevin/.hermes/brain --no-embed
gbrain embed --stale
```

If `gbrain embed --stale` says `expected 1536 dimensions, not 768`, the DB schema was initialized before the Ollama config took effect. Backup/rebuild the PGLite DB with the `gbrain init --pglite --embedding-model ... --embedding-dimensions 768` flags, then import and embed.
