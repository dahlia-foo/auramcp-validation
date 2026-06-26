# SURF 2026 timeline

This is a week-by-week log of my SURF 2026 fellowship (June 2 – July 31, 2026, Strachan Research Group,
Network for Computational Nanotechnology, Purdue). My mentor was Juan Carlos Verduzco (JC), and the PI was
Dr. Alejandro Strachan.

The project was **AURAMCP**, an HTTP MCP server built by JC, Daniel Mejia, and Mohnish Harwani. It exposes
nanoHUB Sim2L workflows to any MCP-compatible agent through a search → describe → execute tool chain
(`search_nanohub_tools` → `get_tool_metadata` → `run_sim2l` → `get_job_status` → `get_job_result`). JC came up
with the MCP concept. My role was testing and validation.

Dates are approximate ("on or around"). This repo was assembled in September 2026, and each commit is dated to
the entry it adds; see the [README](../README.md#about-this-repos-history).

## Late June (weeks 3–5): testing AURA's case studies

- Ran AURA's published case studies and documented the failures: a py3Dmol import failure, recurring
  `getToolMetadata` failures on MeltHEAs (seen by a lab peer too), and a stalled h-BN elastic tensor run.
- After the config was saved post-launch, no trace showed up in LangSmith. I reported it.
- Used a documentation protocol based on a `skills.md` Claude Skill that a peer had set up.
