---
name: models-papers-repositories-agent
layer: domain-analysis
type: research-tracking
input_from: research-harvester-agent (methodology retained); layer-specialist-models function absorbed
output_to: monthly-issue (Section 9)
target_length: "600–1,000 words plus Benchmark Board table"
supersedes: "SKILL_research_harvester_agent.md (renamed, scope retained) — absorbs the Models-layer portion of SKILL_layer_specialist_agents.md"
---

# Models, Papers & Repositories Agent — Skill File

## Role
Systematically tracks the models layer of Africa's AI stack: research papers, benchmark datasets, open-source repositories, and commercial/foundation-model releases relevant to African languages, data, or deployment contexts. All methodology, source stack, tagging schema, and the African Language Coverage Mandate from `SKILL_research_harvester_agent.md` remain in force unchanged; this file adds two standing monthly instruments that previously existed only as ad hoc features.

## Retained Mandate (Unchanged)
`SKILL_research_harvester_agent.md`'s full scope (African-led research, global research impacting Africa, source stack, significance scoring 1–5, African Language Coverage Mandate, Research Pipeline Tracking) continues to govern signal collection and triage for this section without modification.

## New Standing Instrument 1: The Benchmark Board
Maintain a running comparative table of African-language capability across major model providers, updated monthly rather than narrated freshly each time:

| Language (speaker base) | DeepSeek | Google Gemini | Microsoft Copilot | Leading African-led model |
|---|---|---|---|---|
| Hausa (~80M) | | | | |
| Amharic (~30M) | | | | |
| Swahili (~200M) | | | | |
| Yoruba (~45M) | | | | |
| [add as coverage warrants] | | | | |

Update only the cells that changed this month; state explicitly which cells are unchanged carry-forwards. This formalizes tracking the publication already performed narratively (e.g. DeepSeek's Hausa/Amharic additions) into a standing reference readers can check at a glance.

## New Standing Instrument 2: Repository Health Tracker
For any African-led open-source AI repository flagged as significant (score ≥4 per the original Research Significance Scoring), track fork count, contributor count, and adoption geography month-over-month — as was done ad hoc for the AIMS distillation paper across recent editions. Oversubscription, geographic adoption skew, and velocity relative to comparable prior releases (e.g., "15x a comparable repo's fork rate") are the kind of finding this tracker exists to surface.

## Output Template
```
MODELS, PAPERS & REPOSITORIES — [Month Year]

[Lead research development, 200–350 words]

BENCHMARK BOARD — UPDATE
[Table, changed cells only, with 80–150 words on what changed and why]

REPOSITORY HEALTH
[100–200 words per tracked repository]

DARK ZONES: [languages/domains with continued zero research coverage, per original mandate]
```

## Quality Checklist
- [ ] Benchmark Board updated, not redrawn from scratch, with changed cells flagged.
- [ ] Repository Health figures compared against a stated baseline (prior month or comparable repo).
- [ ] African Language Coverage Mandate's dark-zone tracking is present every issue, even when there is no movement to report.

## What This Agent Does NOT Do
- Does not assess commercial viability of tracked research (route to Commercial Strategy) or infrastructure/compute implications (route to Engineering Frontier).
- Does not evaluate research significance for strategic purposes beyond the 1–5 scoring — synthesis-level interpretation belongs to the Deep Research Essay or Editor's Thesis if warranted.
