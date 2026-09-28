# Bugs found and reported (summer 2026)

During testing I found these issues and reported them to the AURAMCP developers or to nanoHUB. **The fixes
were made on their side.** My part was finding each bug, isolating it, and reporting it. Dates are
approximate. Credentials have been removed.

## 1. `Materials-Project-MCP:get_structure` fails on every input

- **Found:** ~Jul 15, during the first h-BN attempt
- **Symptom:** every call returned `list indices must be integers or slices, not str`
- **Isolation:** by ~Jul 20 I had confirmed it on all six BN polymorphs and on mp-149 (Si), so it was not
  specific to one material. I sent JC the full verbatim transcript.
- **Workaround:** build the structure by hand from `fetch_material` output (used for the h-BN run on Jul 21)
- **Status:** worked again by ~Jul 29

## 2. `AURAMCP:run_sim2l` on `cellrelaxdft` rejects dict `structure_dict` input

- **Found:** ~Jul 15
- **Symptom:** passing `structure_dict` as a dict failed with a misleading `missing chosen_outputs` error,
  even though `chosen_outputs` was supplied
- **Isolation:** bisection on the inputs. It reproduced even with a minimal single-site structure dict, so the
  structure itself wasn't the cause. I exported the session log to JC as the bug report.
- **Status:** reported fixed ~Jul 21. The h-BN pipeline ran that day.

## 3. `elasticdft` job returns `not_found` (flagged, not broken)

- **Seen:** Jul 21. The first elasticdft job disappeared after about 35 minutes (session TTL). A resubmission
  finished normally.
- **Reported as:** "sometimes needs a retry", not a hard failure

## 4. AURA client: no LangSmith trace after saving config

- **Found:** late June, while testing AURA's case studies
- **Symptom:** after the config was saved post-launch, no trace appeared in LangSmith

## 5. nanoHUB server errors

- **Reported:** week ending Jul 10, as a nanoHUB support ticket with the server-error logs attached

## 6. Gilbreth "Failed to Connect" (environment issue, not an AURAMCP bug)

- **Jul 8.** I debugged this on a peer's Gilbreth setup. There were two causes, layered on each other: a stale
  editable `mp_api` 0.46.0 that imported `BSPathType`, which emmet-core 0.87.1 no longer has; and a
  per-project `~/.claude.json` entry pointing at the wrong conda env.
- Full write-up: [gilbreth-troubleshooting-report.md](gilbreth-troubleshooting-report.md). Reusable
  checklist: [gilbreth-runbook.md](gilbreth-runbook.md).
