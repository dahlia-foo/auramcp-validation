# AURAMCP validation (SURF 2026)

This repo reproduces and documents the validation work I did on **AURAMCP** as a SURF 2026
fellow (June 2 – July 31, 2026) in the Strachan Research Group / Network for Computational
Nanotechnology (NCN) at Purdue.

## What AURAMCP is

[AURAMCP](https://nanohub.org/tools/auramcp) is an MCP server that exposes nanoHUB simulation
tools (Sim2Ls), nanoHUB ResultsDB, and Materials Project to LLM clients. It follows a
**search → describe → execute** pattern (`search_nanohub_tools` → `get_tool_metadata` →
`run_sim2l` / `get_data_from_nanohub`). It does not register one tool per Sim2L. It builds on
**AURA**, a multi-agent system on LangGraph with a Supervisor plus nanoHUB, Materials Project,
and Code Execution agents
([paper](https://chemrxiv.org/doi/full/10.26434/chemrxiv-2025-rs07k/v2)).

**AURAMCP was built by Juan Carlos Verduzco, Daniel Mejia, and Mohnish Harwani.** Juan Carlos
Verduzco came up with the MCP concept. I did not write the server code.

## My role

I was a backend tester and validator. I:

- ran end-to-end science workflows through AURAMCP (below) to check the results against
  expectations
- found, isolated, and reported bugs to the AURAMCP developers, who made the fixes
- set up AURAMCP for three researchers, twice, and wrote a debugging runbook for the Gilbreth
  cluster
- made the project poster

## Workflows

See the [timeline](docs/timeline.md) as the summer goes.

## About this repo's history

I assembled this repo in September 2026 from files I kept from the summer. **Commits dated June–July 2026 are
backdated.** Each one is dated to when the original work happened, following the
[timeline](docs/timeline.md). Those commits contain the original July files: ResultsDB data, the predictor script,
viewers, session logs, the runbook, and the poster. They also add each timeline entry. The reproduction code
(the MeltHEAs notebook, `extract_plddt.py`, `vrh_moduli.py`) and the write-ups were written in September and
carry their real dates.

## Links

- AURAMCP: https://nanohub.org/tools/auramcp
- AURA paper: https://chemrxiv.org/doi/full/10.26434/chemrxiv-2025-rs07k/v2
