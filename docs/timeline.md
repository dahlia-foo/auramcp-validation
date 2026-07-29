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

## ~Jun 30: week-4 abstract

- Drafted the round-up abstract, "Expanding and Evaluating Autonomous Scientific Workflows on nanoHUB," for
  mentor review.

## ~Jul 2: lab blog post

- Wrote the catch-up blog post covering weeks 3–5.

## ~Jul 6: registering the MCP servers

- Registered the `auramcp` and `nanohubdemo` HTTP servers in Claude Code.
- Fixed connection failures caused by the auth header, which needs the `Bearer` prefix.
- Settled on `claude mcp remove` followed by `claude mcp add` for updating an existing entry.

## ~Jul 8: Gilbreth "Failed to Connect"

- Debugged a peer's Materials Project MCP connection on Purdue's Gilbreth cluster. There were two layered causes:
  a stale editable `mp_api` 0.46.0 install (it imported `BSPathType`, which emmet-core 0.87.1 no longer has),
  and a per-project `~/.claude.json` pointing at the wrong conda env.
- Wrote a progress report for JC and a reusable runbook ([report](gilbreth-troubleshooting-report.md),
  [runbook](gilbreth-runbook.md)).
- Week ending Jul 10: filed a nanoHUB ticket with server-error logs.

## ~Jul 9: paper structure

- Mapped the project onto an IMRaD (Introduction, Methods, Results, Discussion) outline and planned the figures.

## ~Jul 13: reading

- Summarized JC and Dr. Strachan's paper evaluating LLM-generated LAMMPS code (*Computational Materials Science*,
  June 2026).

## ~Jul 15: first h-BN attempt, two bugs reported

- `Materials-Project-MCP:get_structure` failed on every input (`list indices must be integers or slices, not str`).
- `AURAMCP:run_sim2l` on `cellrelaxdft` failed whenever `structure_dict` was a dict, with a misleading
  "missing `chosen_outputs`" error. I isolated it by bisection; it reproduced with a minimal single-site dict.
- No DFT ran. I exported the session log to JC as a bug report. Details: [bug-reports.md](bug-reports.md).

## ~Jul 17: MeltHEAs pipeline and first ESMFold run

- Pulled 2,000 successful MeltHEAs runs from ResultsDB (Coexistence = 1, Converged = 1). Found that
  Tliquid = 2 × Tsolid holds as a fixed convention in this data.
- Fit a no-intercept linear model (rule of mixtures): test R² 0.983, MAE 19.2 K. Ridge, polynomial, random forest,
  and gradient boosting did no better.
- Confirmed Cr0.15 Co0.15 Cu0.35 Fe0.15 Ni0.20 had no existing runs (`find_novel_datapoints`), then ran it live:
  **Tm = 1891.7 ± 1.8 K**. → [`workflows/melthea/`](../workflows/melthea/)
- Ran ESMFold (`proteindl`) on E. coli asparagine synthetase A and saved the 3Dmol backbone viewer.
  → [`workflows/protein/`](../workflows/protein/)
- In-person poster review the same day.

## ~Jul 20: `get_structure` confirmed systemic

- It failed on all six BN polymorphs and on mp-149 (Si). I sent JC the full transcript.

## ~Jul 21: h-BN elastic constants

- JC reported the `cellrelaxdft` bug fixed. I built the structure from `fetch_material` by hand, since
  `get_structure` was still down.
- cellrelaxdft: a = 2.5024 Å, c = 7.1534 Å. elasticdft: the first job came back `not_found`, and the retry finished.
- C11 = 820.7, C33 = 3.7 GPa; bulk modulus (VRH) 114.6 GPa. The small interlayer constants are expected from
  PBEsol without vdW. → [`workflows/hbn-elastic/`](../workflows/hbn-elastic/)

## ~Jul 23: AlphaFold comparison

- Ran the same AsnA sequence through AlphaFold (`alphafold231`), which needed retries after the job expired.
  Mean pLDDT was 97.95, vs. 90.19 for ESMFold.
- The Kabsch Cα RMSD between the two predictions was 0.62 Å.

## ~Jul 24: poster revisions

- Poster text and audit, v3 through v5. Made the ribbon-cartoon ESMFold view for the poster.
- Two practice presentations the next morning.

## ~Jul 28: poster v6

- Added three Sim2L task cards: MeltHEAs, ESMFold/AlphaFold2, and elastic constants.

## ~Jul 29: final poster and h-BN re-run

- Final poster: "AURAMCP: Enhancing nanoHUB's FAIR Workflows and Data through MCP Servers" → [`poster/`](../poster/)
- h-BN re-run: `get_structure` worked again. `cellrelaxdft` succeeded. `elasticdft` was still running when the
  session ended.
