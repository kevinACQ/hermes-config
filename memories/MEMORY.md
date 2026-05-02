User environment constraint: work laptop without admin access; prefers OAuth-based auth over API keys (currently no Anthropic/OpenAI API keys).
§
User now has a GitHub-backed Hermes config backup repo at github.com/kevinACQ/hermes-config, mirrored locally at ~/.hermes/external-repos/hermes-config.
§
Voice onboarding project correction: Alex voice quality is good enough; main blockers are high-quality data ingestion, high-quality output, persistent member memory, and backend database sync.
§
Kevin's default Hermes gateway on macOS is a launchd user agent labeled ai.hermes.gateway with plist at ~/Library/LaunchAgents/ai.hermes.gateway.plist; restart fixes should use launchctl bootout/bootstrap/kickstart rather than pkill because KeepAlive can auto-revive and race gateway.pid cleanup.
§
Claude Code project hub auto-refresh is installed: script at ~/.hermes/scripts/refresh_claude_code_projects.py scans ~/projects and updates ~/.hermes/workspace/claude-code-projects; cron job 'Refresh Claude Code project hub' runs hourly with local-only delivery.