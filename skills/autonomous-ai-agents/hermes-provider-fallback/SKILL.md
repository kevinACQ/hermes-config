---
name: hermes-provider-fallback
description: Configure Hermes provider fallback chains and credential pool strategies, including direct Anthropic fallback from OpenAI Codex.
version: 1.0.0
author: Hermes
license: MIT
metadata:
  hermes:
    tags: [hermes, configuration, fallback, credential-pools, models]
---

# Hermes Provider Fallback

Use this when the user wants Hermes to default to one model/provider but automatically switch to another provider after exhaustion, rate limits, overload, or connection failures.

## Key facts

- Hermes supports ordered provider fallback via the top-level `fallback_providers` list.
- The legacy `fallback_model` setting is a single fallback dict; prefer `fallback_providers` for new work.
- Credential-pool rotation strategy is controlled by top-level `credential_pool_strategies`, keyed by provider.
- `fill_first` means Hermes keeps using the first available credential until it is exhausted, then moves to the next available credential.
- Direct Anthropic model IDs use hyphen style such as `claude-sonnet-4-6`; OpenRouter-style IDs such as `anthropic/claude-sonnet-4.6` are for OpenRouter-like providers, not the direct Anthropic provider.

## Example target state

For a user who wants OpenAI Codex GPT 5.5 as primary and direct Anthropic Sonnet 4.6 as fallback, the relevant config shape is:

```yaml
model:
  default: gpt-5.5
  provider: openai-codex
  base_url: https://chatgpt.com/backend-api/codex
fallback_providers:
- provider: anthropic
  model: claude-sonnet-4-6
credential_pool_strategies:
  openai-codex: fill_first
  anthropic: fill_first
```

## Verification checklist

1. Confirm the config has the intended primary model/provider and fallback list.
2. Run Hermes config validation.
3. Check that each relevant provider has at least one credential in its pool and `has_available()` is true.
4. Instantiate `AIAgent` with the loaded fallback config in quiet mode and confirm `_fallback_chain` contains the expected fallback dict.
5. If the user keeps a Git-backed Hermes config backup, sync and commit the updated config backup after verifying.
6. Tell gateway or Telegram users to restart the gateway before expecting the new config to apply there.

## Pitfalls

- Do not assume an environment variable key exists; OAuth and auth-store credential pools may be present even when `.env` has no provider API key.
- Do not use `anthropic/claude-sonnet-4.6` for direct Anthropic. Use `claude-sonnet-4-6`.
- Config changes affect new sessions; running CLI or gateway processes may need restart or a fresh session.
