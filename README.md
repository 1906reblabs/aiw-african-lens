# AIW African Lens Monthly Intelligence Review

**Institutional-grade intelligence on Africa's AI stack.** Published the last Wednesday of every month at 06:00 SAST.

This repository contains the editorial pipeline, build system, and published archive for AIW African Lens. As of the transition date, the publication has moved from a weekly cadence (Volume I, AIW-026-01 through AIW-026-13) to a monthly format (Volume II, beginning AIW-2026-07) with a substantially deepened eleven-section issue structure. See `MIGRATION_NOTES_weekly_to_monthly.md` for the full transition record.

## What This Publication Is
A monthly intelligence review tracking AI policy, infrastructure, capital, research, and geopolitics across all 54 African Union member states, targeting investors, policymakers, technology executives, researchers, and founders. Benchmarked editorially against Bloomberg Intelligence, MIT Technology Review, Stratechery, McKinsey Technology Trends, SemiAnalysis, and RAND — see `SKILL_monthly_editorial_architecture.md` for the full rationale and section-by-section model mapping.

## Issue Structure (Volume II)
1. Editor's Thesis
2. Executive Brief
3. Signals & Metrics
4. Deep Research Essays (1–2)
5. Engineering Frontier
6. Commercial Strategy
7. Policy & Geopolitics
8. African Builders
9. Models, Papers & Repositories
10. Scenarios & Forecasts
11. Reading List

Target length: ~10,600–16,200 words per issue.

## Repository Structure
```
content/
  registry.yaml                 — master index of all editions (weekly archive + monthly going forward)
  issues/
    aiw-026-NN-content.md       — Volume I weekly content files (archived)
    aiw-2026-MM-content.md      — Volume II monthly content files (new schema — see below)
templates/
  issue.j2                      — HTML template (requires update for 11-section monthly schema — see below)
  index.j2                      — archive/index page template
afi_parser.py                   — YAML → template-context parser (requires field-processor updates)
build.py                        — build orchestrator (CLI: issue / index / all)
.github/workflows/build.yml     — GitHub Actions: auto-build on push, commits docs/ output
```

## Editorial Pipeline (Agent Architecture)
The publication is produced by a multi-agent reasoning pipeline run via Claude with a structured set of skill files, one per agent role. Skill files live at the project root and are read by the operating Claude session before any task in that agent's domain.

**Perception layer** (continuous signal collection): `SKILL_geo_scraper_agent.md`, `SKILL_policy_regulation_agent.md`, `SKILL_research_harvester_agent.md`, `SKILL_startup_capital_tracker.md`, `SKILL_infra_signals_agent.md` — cadence updated for monthly via `SKILL_perception_layer_monthly_addendum.md`.

**Validation layer:** `SKILL_research_analyst_agent.md` — cadence updated via the same addendum.

**Domain analysis layer:** `SKILL_engineering_frontier_agent.md`, `SKILL_commercial_strategy_agent.md`, `SKILL_policy_geopolitics_strategist.md`, `SKILL_models_papers_repositories_agent.md`.

**Strategic/narrative layer:** `SKILL_scenarios_forecasts_agent.md`, `SKILL_deep_research_essay_agent.md`, `SKILL_african_builders_agent.md`, `SKILL_reading_list_curator_agent.md`.

**Summary layer:** `SKILL_executive_brief_agent.md`, `SKILL_editors_thesis_agent.md`.

**Orchestration:** `SKILL_synthesis_agent_v2.md` (Editor-in-Chief AI) — sequences all of the above per the production calendar in `SKILL_monthly_editorial_architecture.md`, then hands the assembled draft to the human operator.

See `MIGRATION_NOTES_weekly_to_monthly.md` for the full mapping from the original weekly-format skill files to the new architecture, including which originals are retained as live methodology references inside the new files.

## Production Calendar (per issue)
Day 1–21: continuous signal collection. T-14d: essay topic shortlist. T-10d: validation freeze, domain analysis begins. T-7d: scenarios/essay/profiles drafted. T-4d: full synthesis. T-2d: human review. Last Wednesday: publish. Full detail in `SKILL_monthly_editorial_architecture.md`.

## Required Engineering Changes (Not Yet Implemented)
The eleven-section monthly structure requires changes to the build pipeline beyond the editorial skill files in this repository:

1. **`afi_parser.py`** — add field processors for the new content-file sections (`editors_thesis`, `executive_brief`, `signals_metrics`, `deep_research_essays` [list], `engineering_frontier`, `commercial_strategy`, `policy_geopolitics`, `african_builders` [list], `models_papers_repos`, `scenarios_forecasts` [list], `reading_list` [list]), replacing/extending the Volume I processors (`_process_signals`, `_process_layers`, etc.).
2. **`templates/issue.j2`** — new monthly layout template; the existing weekly template's section ordering and visual hierarchy (signal-card, layer-grid, fragility-card, contrarian-card components) can largely be reused/relabeled for the new section names, but the eleven-section sequence and the standing Benchmark Board / KPI table components are new.
3. **`content/registry.yaml`** — add a `monthly:` list alongside the existing `weekly:` list, or migrate to a unified schema with a `cadence: weekly | monthly` field per entry, to keep the Volume I archive browsable alongside Volume II.
4. **Edition numbering** — registry and file-naming conventions move from `aiw-026-NN` to `aiw-YYYY-MM`.

These are available as a follow-up engineering task — ask to have `afi_parser.py`, `build.py`, and `templates/issue.j2` updated directly once the new content schema is finalized.

## Monetisation Context
This restructuring supports the publication's existing monetisation plans (institutional subscription tiers, sponsored country spotlights, bespoke briefs). The standing KPI table in Signals & Metrics is the seed of the previously planned Annual Pan-African AI Index — see `SKILL_monthly_editorial_architecture.md`, Monetisation Note.

## Other Properties
A separate publication, `ekurhuleni-underground`, is maintained in a separate repository and is out of scope for this migration.
