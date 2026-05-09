User environment constraint: work laptop without admin access; prefers OAuth-based auth over API keys (currently no Anthropic/OpenAI API keys).
§
User now has a GitHub-backed Hermes config backup repo at github.com/kevinACQ/hermes-config, mirrored locally at ~/.hermes/external-repos/hermes-config.
§
Voice onboarding project correction: Alex voice quality is good enough; main blockers are high-quality data ingestion, high-quality output, persistent member memory, and backend database sync.
§
Kevin's default Hermes gateway on macOS is a launchd user agent labeled ai.hermes.gateway with plist at ~/Library/LaunchAgents/ai.hermes.gateway.plist; restart fixes should use launchctl bootout/bootstrap/kickstart rather than pkill because KeepAlive can auto-revive and race gateway.pid cleanup.
§
Claude Code project hub auto-refresh is installed: script at ~/.hermes/scripts/refresh_claude_code_projects.py scans ~/projects and updates ~/.hermes/workspace/claude-code-projects; cron job 'Refresh Claude Code project hub' runs hourly with local-only delivery.
§
Kevin's Claude knowledge base lives at /Users/kevin/projects/cog-config/knowledge-base. Symlinks exist at /Users/kevin/.claude/knowledgebase and /Users/kevin/.hermes/knowledgebase. Claude skill /Users/kevin/.claude/skills/kb-add/SKILL.md defines the ingest workflow.
§
GBrain on Kevin's macOS: if CLI/MCP fails with a PGLite WASM runtime error, first test a temp PGLite brain. On 2026-05-08 the fix was to backup/rebuild ~/.hermes/.gbrain/brain.pglite from /Users/kevin/.hermes/brain markdown and run gbrain apply-migrations; embeddings still require a configured embedding provider/API key.
§
Kevin's MacBook has Ollama installed user-space at ~/Applications/Ollama.app with CLI symlink ~/.local/bin/ollama; nomic-embed-text is pulled and serves on localhost:11434. GBrain local PGLite is configured with ollama:nomic-embed-text at 768 dimensions and shows 100% embed coverage. Avoid Ollama prompts to move/update into /Applications because work laptop lacks admin access.