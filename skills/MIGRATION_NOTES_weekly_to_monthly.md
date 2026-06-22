---
name: migration-notes
type: reference
status: "one-time transition document — Volume I (weekly) to Volume II (monthly)"
---

# Migration Notes — Weekly to Monthly Transition

## File Status Table

| File | Status | Action |
|---|---|---|
| SKILL_geo_scraper_agent.md | Retained, cadence-patched | Keep; apply `SKILL_perception_layer_monthly_addendum.md` |
| SKILL_policy_regulation_agent.md | Retained, cadence-patched | Keep; apply addendum |
| SKILL_startup_capital_tracker.md | Retained, cadence-patched | Keep; apply addendum |
| SKILL_infra_signals_agent.md | Retained, cadence-patched | Keep; apply addendum |
| SKILL_research_analyst_agent.md | Retained, cadence-patched | Keep; apply addendum |
| SKILL_research_harvester_agent.md | Superseded | Replace active use with `SKILL_models_papers_repositories_agent.md`; retain as methodology reference (source stack, significance scoring unchanged within it) |
| SKILL_layer_specialist_agents.md | Superseded | Replace active use with `SKILL_engineering_frontier_agent.md` (Energy/Chips/Infra), `SKILL_models_papers_repositories_agent.md` (Models), `SKILL_commercial_strategy_agent.md` (Applications). Retain as historical reference for the 1st/2nd/3rd-order framework, which all three successors inherit. |
| SKILL_policy_regulation_strategist.md | Superseded (renamed) | Replace active use with `SKILL_policy_geopolitics_strategist.md`, which extends rather than replaces this file's mandates |
| SKILL_taleb_agent.md | Superseded (merged) | Replace active use with `SKILL_scenarios_forecasts_agent.md`; retain as the canonical reference for the Fragility Assessment template |
| SKILL_thiel_agent.md | Superseded (merged) | Replace active use with `SKILL_scenarios_forecasts_agent.md`; retain as the canonical reference for the Contrarian Bet Assessment template |
| SKILL_synthesis_agent.md | Superseded (v2) | Replace with `SKILL_synthesis_agent_v2.md` |
| (none — new) | New | `SKILL_monthly_editorial_architecture.md`, `SKILL_editors_thesis_agent.md`, `SKILL_executive_brief_agent.md`, `SKILL_signals_metrics_agent.md`, `SKILL_deep_research_essay_agent.md`, `SKILL_african_builders_agent.md`, `SKILL_reading_list_curator_agent.md` |

**Recommendation:** upload all new/updated files to the Claude Project; do not delete the five superseded files (`layer_specialist_agents`, `research_harvester` (old), `taleb`, `thiel`, `policy_regulation_strategist`, `synthesis_agent` v1) — they remain valid methodology references that the new files explicitly cite and inherit from. Deleting them would orphan those references.

## Edition Numbering Transition
**Volume I (weekly):** AIW-026-01 through AIW-026-13, final window closing 2 June 2026. This archive is permanent and unchanged.

**Volume II (monthly)** begins with **AIW-2026-07** (July 2026), recommended as an **Inaugural Monthly Issue** with an expanded window — 3 June 2026 through 29 July 2026 (~8 weeks) — explicitly framed editorially as a relaunch issue covering the transition period, rather than silently skipping or compressing six weeks of signal collection. Subsequent issues (AIW-2026-08 onward) revert to the standard last-Wednesday-to-last-Wednesday window (4–5 weeks).

Edition code format: **AIW-YYYY-MM**. This is a deliberate break from the sequential weekly numbering (AIW-026-NN) because monthly cadence maps naturally onto calendar months and sorts correctly without a running counter.

## index.md / registry.yaml Implications
The registry schema (the `weekly:` list in `index.md`) will need a parallel or successor structure for monthly editions — recommend a new top-level key, e.g. `monthly:`, with fields mirroring the existing weekly entry shape (id, status, badge, date, window, title, subtitle, summary, themes_line, developments, file) plus new fields for the eleven-section structure (see `README_v2_monthly.md` for the proposed content-file schema). This is a build-pipeline change to `afi_parser.py`, `build.py`, and `templates/issue.j2` — not addressed in these skill files, since it is engineering rather than editorial work. Flagged here for visibility; available as a follow-up task.
