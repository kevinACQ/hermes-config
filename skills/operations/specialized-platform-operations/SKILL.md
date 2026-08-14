---
name: specialized-platform-operations
description: "Operate and troubleshoot specialized platforms and local tools: Hermes Agent, ComfyUI, TouchDesigner, Jupyter, Obsidian, Philips Hue/OpenHue, Retell-style voice calls, X/Twitter via xurl, Yuanbao groups, and authorized LLM red-team harnesses. Use whenever one of these named systems or its workflows is involved."
version: 1.0.0
author: Hermes Agent
license: MIT
platforms: [linux, macos, windows]
metadata:
  hermes:
    tags: [platform-operations, hermes, comfyui, touchdesigner, jupyter, obsidian, hue, voice-calls, xurl, yuanbao, red-teaming]
---

# Specialized Platform Operations

Use this class-level skill for operational workflows tied to a named platform, CLI, local application, or provider. Start with the routing table, then load only the relevant reference. Each reference preserves the former specialist skill's full instructions; its support files are namespaced under the umbrella's canonical directories.

## Routing

| User intent or system | Load this reference | Support files |
|---|---|---|
| Configure, extend, contribute to, or troubleshoot Hermes Agent | `references/hermes-agent.md` | `references/hermes-agent/` |
| Install or operate ComfyUI; execute image/video/audio workflows | `references/comfyui.md` | `references/comfyui/`, `scripts/comfyui/`, `templates/comfyui/workflows/` |
| Control TouchDesigner through twozero MCP | `references/touchdesigner-mcp.md` | `references/touchdesigner-mcp/`, `scripts/touchdesigner-mcp/` |
| Use a stateful Jupyter kernel for iterative Python | `references/jupyter-live-kernel.md` | none |
| Read, search, create, or edit an Obsidian vault | `references/obsidian.md` | none |
| Control Philips Hue with OpenHue CLI | `references/openhue.md` | none |
| Place or simulate outbound AI voice calls and resolve private aliases | `references/voice-calling-operations.md` | `references/voice-calling-operations/` |
| Read or mutate X/Twitter through the official xurl CLI | `references/xurl.md` | none |
| Mention, query, or DM Yuanbao group members | `references/yuanbao.md` | none |
| Run authorized LLM red-team or refusal-resilience experiments | `references/godmode.md` | `references/godmode/`, `scripts/godmode/`, `templates/godmode/` |

## Shared Operating Standard

1. Load the platform reference before acting; tool names, authentication rules, and version-specific pitfalls vary.
2. Run prerequisite discovery first: executable availability, auth/status checks that do not expose secrets, server reachability, and exact target resolution.
3. Never read secrets or credential stores into model context. Ask the user to complete secret-bearing setup outside the agent session when the platform requires it.
4. Separate read-only discovery from external mutations. Confirm scope for posts, DMs, calls, deletions, purchases, reservations, or other consequential actions.
5. Execute the real workflow and verify with a platform-native ID, status response, output artifact, screenshot, transcript, or health check before reporting success.
6. Prefer the bundled deterministic scripts and templates over rewriting one-off probes.

## Platform Sections

### Hermes Agent
Load `references/hermes-agent.md`. Treat the live documentation at https://hermes-agent.nousresearch.com/docs as authoritative when it differs from the bundled reference. The re-homed MCP and webhook notes live under `references/hermes-agent/`.

### ComfyUI
Load `references/comfyui.md`. Preserve its local-versus-cloud decision, hardware check, API-format workflow requirement, dependency validation, and output verification. Reusable scripts live under `scripts/comfyui/`; workflow starters live under `templates/comfyui/workflows/`.

### TouchDesigner
Load `references/touchdesigner-mcp.md`. Discover operator parameters and hints before building, prefer native MCP tools, and verify errors, performance, and screenshots. Detailed operator and creative-system notes live under `references/touchdesigner-mcp/`.

### Jupyter
Load `references/jupyter-live-kernel.md` when state must persist across Python executions. Use one-shot `execute_code` or shell commands instead when persistent notebook state is unnecessary.

### Obsidian
Load `references/obsidian.md`. Resolve the concrete vault path first, then use native file tools for reads, searches, writes, and patches.

### Philips Hue
Load `references/openhue.md`. Discover exact room, scene, and light names before issuing control commands; pairing requires physical bridge access.

### Voice Calling
Load `references/voice-calling-operations.md`. Keep phone numbers private, distinguish real calls from simulations, obtain a real provider call ID, and verify final status or transcript evidence.

### X / Twitter
Load `references/xurl.md`. Never inspect `~/.xurl`, pass inline secrets, or use verbose mode. Verify auth status safely and confirm every write action's target and intent.

### Yuanbao
Load `references/yuanbao.md`. Resolve exact nicknames before @mentions; use the Yuanbao-native DM tool rather than generic cross-platform messaging.

### Authorized LLM Red-Teaming
Load `references/godmode.md` only for authorized evaluation of model refusal behavior and prompt robustness. Keep tests scoped to systems the user owns or is permitted to assess; do not use the material to facilitate harmful real-world activity.

## Verification Checklist

- [ ] Correct platform reference loaded.
- [ ] Prerequisites and target identity discovered.
- [ ] No secrets or private identifiers exposed.
- [ ] Consequential action scope confirmed where needed.
- [ ] Real action executed with the platform's intended tool or script.
- [ ] Result verified through concrete platform evidence.
