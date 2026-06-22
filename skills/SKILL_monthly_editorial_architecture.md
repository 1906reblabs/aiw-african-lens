---
name: monthly-editorial-architecture
layer: meta
type: editorial-structure
version: "2.0"
status: "active — supersedes weekly cadence (AIW-026-01 through AIW-026-13)"
applies_to: all agents
---

# Monthly Editorial Architecture — Skill File

## Masthead

**Title:** AIW African Lens Monthly Intelligence Review
**Tagline:** Institutional-grade intelligence on Africa's AI stack — for the people building, funding, and governing it.
**Cadence:** Monthly, published the last Wednesday of every month, 06:00 SAST.
**Edition code:** AIW-YYYY-MM (e.g. AIW-2026-07 for the July 2026 issue). Replaces the sequential weekly numbering (AIW-026-01 → AIW-026-13), retired and archived as Volume I.
**Distribution:** GitHub Pages (canonical), Substack (subscriber-facing).

## Why Monthly

A weekly cadence forces a news-recap posture: by the time analysis is good enough to be worth a subscriber's hour, the week's events have already moved on. None of the publications this product is benchmarked against — Bloomberg Intelligence, MIT Technology Review, Stratechery, McKinsey Technology Trends, SemiAnalysis, RAND — publish meaningful original research weekly. They publish on cycles long enough to let an analyst find the second- and third-order story, and they charge accordingly. Monthly cadence is not a step down in ambition; it is the precondition for the kind of analysis this publication has always claimed to deliver.

The weekly archive (Volume I) is not deleted. It remains the publication's evidentiary backbone — the day-by-day record that monthly essays, scenarios, and the Signals & Metrics dashboard now draw on as a verified data layer, the way a RAND report draws on primary-source intelligence reporting it does not itself republish.

## Benchmark Publications — What Each Lends This Product

| Publication | Cadence | What AIW borrows |
|---|---|---|
| **Bloomberg Intelligence** | Continuous, chart-driven | The Signals & Metrics dashboard: terse, numerate, trend-delta framing. No metric without a number; no number without a trend. |
| **MIT Technology Review** | Monthly/feature | The Deep Research Essay's narrative architecture and the African Builders profile format (their "Innovators" convention, applied with comparable rigor, not flattery). |
| **Stratechery** | Daily/weekly essay, single voice | The Editor's Thesis: one falsifiable argument, stated plainly, tracked across issues. The Reading List's annotated-link convention. |
| **McKinsey Technology Trends / Quarterly** | Periodic, executive-facing | The Executive Brief's "what happened / why it matters / what to watch" triads, and the Commercial Strategy section's operator-facing framing. |
| **SemiAnalysis** | Frequent, deeply technical | The Engineering Frontier's quantitative rigor — units, costs, specifications, supply-chain mapping, no hand-waving about hardware or power. |
| **RAND Corporation** | Reports/Perspectives, scenario-driven | The Policy & Geopolitics section's actor-incentive mapping, and the Scenarios & Forecasts section's explicit, falsifiable, probability-banded scenario construction. |

## The Eleven Sections

| # | Section | Purpose | Model | Target Words | Owning Agent |
|---|---|---|---|---|---|
| 1 | Editor's Thesis | One falsifiable governing argument | Stratechery / RAND Key Judgments | 500–700 | editors-thesis-agent |
| 2 | Executive Brief | Scannable digest, 5–7 items | McKinsey "In Brief" | 600–900 | executive-brief-agent |
| 3 | Signals & Metrics | Standing quantitative dashboard | Bloomberg Intelligence | 700–1,100 (+ tables) | signals-metrics-agent |
| 4 | Deep Research Essays | Marquee long-form argument(s) | MIT Tech Review / SemiAnalysis / Stratechery | 2,500–4,000 ea. (1–2) | deep-research-essay-agent |
| 5 | Engineering Frontier | Energy/Chips/Infra, unified technical narrative | SemiAnalysis | 1,200–1,800 | engineering-frontier-agent |
| 6 | Commercial Strategy | Market structure, operator-facing | McKinsey Quarterly | 1,000–1,500 | commercial-strategy-agent |
| 7 | Policy & Geopolitics | Regulation + great-power dynamics | RAND | 1,200–1,800 | policy-geopolitics-strategist |
| 8 | African Builders | 2–3 rigorous founder/engineer/regulator profiles | MIT TR Innovators | 800–1,200 | african-builders-agent |
| 9 | Models, Papers & Repositories | Research + benchmark + repo tracking | — | 600–1,000 | models-papers-repositories-agent |
| 10 | Scenarios & Forecasts | 2–4 falsifiable, probability-banded scenarios | RAND scenario planning | 1,200–1,800 | scenarios-forecasts-agent |
| 11 | Reading List | 5–10 annotated outside items | Stratechery linked list | 200–400 | reading-list-curator-agent |

**Total issue length: ~10,600–16,200 words excluding tables, code, and footnotes.** This sits between a Stratechery week-in-essays and a slim RAND Perspective — long enough to reward a paid subscription, short enough to be read in one sitting by a senior reader with 60–90 minutes.

## Production Calendar (4–5 Week Cycle)

Window runs from the previous issue's publication Wednesday to the current one.

- **Day 1 – Day ~21:** Continuous perception-layer collection (rolling, not batch-Monday-only — see `SKILL_perception_layer_monthly_addendum.md`).
- **~T-14 days:** Mid-window editorial check-in. Candidate Deep Research Essay topics shortlisted (need ≥2-week lead time to be done properly).
- **~T-10 days:** Research Analyst validation freeze for the month's signal set. Domain analysis begins (Engineering Frontier, Commercial Strategy, Policy & Geopolitics, Models/Papers/Repos).
- **~T-7 days:** Scenarios & Forecasts and African Builders drafted. Deep Research Essay(s) enter first full draft.
- **~T-4 days:** Synthesis Agent assembles the full issue; Editor's Thesis and Executive Brief written last, since they summarize everything else.
- **~T-2 days:** Human operator review.
- **Last Wednesday, 06:00 SAST:** Publish.

## Section Ownership & Dependency Graph

```
PERCEPTION (continuous)
  Geo Scraper · Policy & Regulation Agent · Capital Tracker · Infra Signals · Research Harvester
        ↓
RESEARCH ANALYST (validation freeze, T-10d)
        ↓
DOMAIN AGENTS (T-10d → T-7d)
  Engineering Frontier · Commercial Strategy · Policy & Geopolitics · Models/Papers/Repos
        ↓
STRATEGIC + NARRATIVE AGENTS (T-7d → T-4d)
  Scenarios & Forecasts · Deep Research Essay(s) · African Builders · Reading List
        ↓
SYNTHESIS AGENT (T-4d)
  → assembles all 11 sections, writes Executive Brief + Editor's Thesis last
        ↓
HUMAN OPERATOR (T-2d) → PUBLISH
```

## Continuity Devices

Two devices carry the publication's argument across issues, distinguishing it from a stack of disconnected monthly snapshots:

- **Thesis Tracker** (owned by editors-thesis-agent): every issue's governing thesis is logged with a status the following month — Confirmed / Revised / Abandoned — with the evidence that produced the verdict.
- **Scenario Watchlist** (owned by scenarios-forecasts-agent): every scenario is carried forward until it resolves, with probability revised up or down based on new signals.

## What Distinguishes Monthly Depth From Weekly Recap

A section fails the monthly bar if it could have been written the same week the underlying event happened. Every section must do at least one of: synthesize across the full window rather than re-narrate single events; quantify something the raw news did not quantify; take a position the news coverage did not take; or connect the event to a structural pattern visible only in aggregate.

## Editorial Voice Update

Voice remains senior-analyst, not journalist or marketer (unchanged from Volume I). Monthly cadence licenses a slightly more essayistic register in the Editor's Thesis and Deep Research Essays specifically — first-person analytical voice ("I think," "the evidence here points to") is now permitted in those two sections only, matching the Stratechery and RAND-Perspective convention of a named analytical point of view. All other sections retain the impersonal institutional voice of Volume I.

## Monetisation Note

This restructuring is also a pricing event. A monthly, 10,000+ word, multi-section intelligence review with named scenario forecasts and a standing KPI dashboard supports an institutional subscription price point that a weekly recap cannot. The Signals & Metrics section's standing KPI set is the seed of the previously planned Annual Pan-African AI Index; treat it as a live preview of that product, not a one-off.
