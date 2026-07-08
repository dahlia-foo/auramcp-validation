# Materials Project MCP — Connection Troubleshooting Report

**Date:** July 8, 2026
**Issue:** `materials-project` MCP server showing "Failed to Connect" in Claude Code (both `claude mcp list` and the UI), on a Windows/Gilbreth setup, while working correctly on Mac (local) and for at least one other Gilbreth Windows user.

## Summary

Diagnosed and resolved a "Failed to Connect" error for the `materials-project` MCP server in Claude Code, running on Purdue's Gilbreth HPC cluster. The root cause turned out to be two independent problems layered on top of each other:

1. **A stale/broken `mp_api` install.** The affected user had `mp_api` installed as an editable package from an old git clone (version 0.46.0) rather than from PyPI, while `emmet-core` (a dependency) had been separately upgraded to a much newer version (0.87.1). The old `mp_api` code imported a symbol (`BSPathType`) that no longer existed in the newer `emmet-core`, causing an immediate `ImportError` on server startup.

2. **A misconfigured project directory.** Once the import issue was fixed in one conda environment (`test_env`), Claude Code was still failing to connect — because the MCP server config that Claude Code was actually reading (tied to a *different* project subfolder, `aura_mcp`) pointed at a *different*, still-broken conda environment (`mcp_env`). Claude Code's MCP configs are scoped per project directory, so fixing the environment in one directory's config didn't propagate to another.

## Resolution

- Reinstalled `mp-api` cleanly from PyPI (matching the working version) inside the correct conda environment.
- Confirmed the fix by running the MCP server manually and verifying it started cleanly (FastMCP banner, no traceback).
- Traced Claude Code's actual MCP config in `~/.claude.json` to find the config scoped to the correct working directory, and repointed/re-added the `materials-project` server entry there with the correct Python path and `MP_API_KEY` environment variable.
- Removed the redundant, broken config entry from the incorrect project subfolder to avoid future confusion.
- Confirmed connection success via `claude mcp get materials-project` and `claude mcp list`.

## Key takeaway

"Failed to Connect" in Claude Code is a generic error that can stem from several independent causes — dependency/version mismatches, conda environment inheritance issues, or Claude Code reading the wrong per-project config. The fastest diagnostic path is always to **run the exact configured command manually** (`claude mcp get <server>` to see the command, then run it directly) rather than debugging through Claude Code's UI, since that surfaces the real Python error immediately instead of a generic connection failure message.
