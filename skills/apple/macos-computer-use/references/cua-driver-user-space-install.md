# cua-driver user-space fallback on locked-down macOS

Use this when `computer_use` is enabled in Hermes, but `handle_computer_use` reports that `cua-driver` is missing and the official installer fails because `/Applications` is not writable.

## Probe

From the Hermes repo venv, verify whether the backend sees the driver:

```bash
cd ~/.hermes/hermes-agent
./venv/bin/python - <<'PY'
from tools.computer_use.tool import check_computer_use_requirements, handle_computer_use
print('requirements', check_computer_use_requirements())
print(handle_computer_use({'action':'list_apps'}, task_id=None)[:1000])
PY
```

Expected missing-driver signal:

```text
requirements False
{"error": "computer_use backend unavailable: cua-driver is not installed..."}
```

## Preferred install path

Try the official wrapper first:

```bash
hermes computer-use install
```

On locked-down work laptops this may download successfully but fail at `/Applications/CuaDriver.app` because `/Applications` is not writable.

## User-space fallback

Install only the bare binary into `~/.local/bin`:

```bash
mkdir -p ~/.local/bin /tmp/cua-install-manual
cd /tmp/cua-install-manual
curl -fsSL -o cua.tar.gz \
  https://github.com/trycua/cua/releases/download/cua-driver-rs-v0.5.2/cua-driver-rs-0.5.2-darwin-universal.tar.gz
tar -xzf cua.tar.gz
install -m 0755 cua-driver-rs-0.5.2-darwin-universal/cua-driver ~/.local/bin/cua-driver
~/.local/bin/cua-driver --version
```

If MCP calls hang after printing an update notice, disable update checks for Hermes-launched driver processes:

```bash
printf '\nCUA_DRIVER_RS_UPDATE_CHECK=0\n' >> ~/.hermes/.env
```

Then restart the gateway if the current session is from Telegram/Discord:

```bash
launchctl bootout gui/$(id -u) ~/Library/LaunchAgents/ai.hermes.gateway.plist 2>/dev/null || true
launchctl bootstrap gui/$(id -u) ~/Library/LaunchAgents/ai.hermes.gateway.plist
launchctl kickstart -k gui/$(id -u)/ai.hermes.gateway
```

## Verify

```bash
cd ~/.hermes/hermes-agent
set -a; . ~/.hermes/.env; set +a
./venv/bin/python - <<'PY'
from tools.computer_use.tool import check_computer_use_requirements, handle_computer_use
print('requirements', check_computer_use_requirements())
print(handle_computer_use({'action':'list_apps'}, task_id=None)[:1000])
PY
```

A useful partial-success signal is:

```text
requirements True
{"apps": [], "count": 0}
```

Full desktop capture/control can still require macOS Accessibility and Screen Recording grants. Do not click permission prompts yourself unless the user explicitly asks; stop and ask the user to grant the permissions.

## Notes

- The user-space fallback does not install `CuaDriver.app`, so TCC attribution may differ from the official install.
- Treat this as a fallback for constrained machines, not the default path.
- Do not save a durable memory that `computer_use` is broken; capture the setup fallback instead.
