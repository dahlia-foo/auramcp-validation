# Materials Project MCP — "Failed to Connect" Runbook

Use this checklist when a user's `materials-project` (or any Python-based) MCP server shows "Failed to Connect" in Claude Code. Work top to bottom; stop as soon as you find the failure.

## Step 1 — Get the exact command Claude Code is running
```
claude mcp get materials-project
```
Note the `Command:`, `Args:`, and `Environment:` values exactly.

## Step 2 — Run that exact command manually
```
<command from Step 1> <args from Step 1>
```
Example:
```
/path/to/conda/envs/<env>/bin/python -m mp_api.mcp.server
```
- If it throws an error/traceback → go to Step 3 (dependency issue).
- If it starts cleanly (FastMCP banner appears, no traceback) → go to Step 6 (config/project mismatch).

## Step 3 — Diagnose import/dependency errors
If Step 2 fails with an `ImportError` (e.g. `cannot import name 'X' from 'Y'`):

a. Check whether the failing package is an **editable install from a git clone** vs installed from PyPI:
```
<python path> -m pip show mp-api
```
Look for `Editable project location:` — if present, this is a dev checkout that may be out of sync with other installed dependencies.

b. Check what dependency version range the repo expects:
```
cat <editable project location>/pyproject.toml | grep -i emmet
```

c. Compare against a known-working install (yours, or another working user's):
```
<python path> -m pip show emmet-core
```

## Step 4 — If it's a stale editable install, replace it with the PyPI version
```
<python path> -m pip uninstall mp-api -y
<python path> -m pip install mp-api==<known-working-version> --no-cache-dir
```
Re-verify:
```
<python path> -m pip show mp-api
```
(Should no longer show `Editable project location:`)

## Step 5 — Re-test the import and server
```
<python path> -c "from mp_api.client.mprester import MPRester; print('ok')"
<python path> -m mp_api.mcp.server
```
Should print `ok` and then show the FastMCP startup banner. Ctrl+C to exit (may need to Ctrl+C twice, or kill from a second terminal: `pkill -f mp_api.mcp.server`).

## Step 6 — If the manual run works but Claude Code still fails: check for a project/config mismatch
Claude Code's MCP configs are scoped **per project directory** (stored in `~/.claude.json` under a `projects` key). It's common for a user to have multiple project folders, each with its own (possibly different/stale) config.

a. List every project directory and which Python path its `materials-project` server uses:
```
python3 -c "
import json, os
with open(os.path.expanduser('~/.claude.json')) as f:
    data = json.load(f)
for path, cfg in data.get('projects', {}).items():
    servers = cfg.get('mcpServers', {})
    if 'materials-project' in servers:
        print(path, '->', servers['materials-project']['command'])
"
```

b. Identify which directory the user is actually launching Claude Code from, and confirm it matches the environment you just fixed.

c. `cd` into the correct directory and confirm:
```
claude mcp get materials-project
```

d. If it's pointing at the wrong/broken environment, remove and re-add with the correct path and API key:
```
claude mcp remove materials-project -s local
claude mcp add materials-project --env MP_API_KEY=<key> -- <correct python path> -m mp_api.mcp.server
```
(Check `claude mcp add --help` if the `--env` flag syntax differs.)

e. Clean up any redundant/broken duplicate entries in other project subfolders to avoid future confusion:
```
cd <other project folder>
claude mcp remove materials-project -s local
```

## Step 7 — Verify
```
claude mcp get materials-project
claude mcp list
```
Both should now show the correct Python path and a successful connection.

## Fast triage cheat sheet
| Symptom | Likely cause |
|---|---|
| Manual run throws `ImportError` | Stale/editable dependency install — go to Step 3 |
| Same version number, different import behavior between two users | Corrupted/partial pip install — try `pip uninstall` **twice**, manually `rm -rf` the leftover package folder in `site-packages`, then reinstall with `--no-cache-dir` |
| Manual run works, Claude Code still fails | Wrong project directory / stale per-project config — go to Step 6 |
| `claude mcp get` shows correct command but still fails | Restart Claude Code fully (not just retry); check `~/.claude.json` for the actual per-project entry being used |
| Windows-specific `'python' is not recognized` | `command` field uses bare `python` instead of a full absolute path — always use the full path to the env's Python binary |
