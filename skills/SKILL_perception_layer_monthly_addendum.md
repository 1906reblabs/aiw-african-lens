---
name: perception-layer-monthly-addendum
layer: perception
type: cadence-patch
applies_to: geo-scraper-agent, policy-regulation-agent, startup-capital-tracker, infra-signals-agent, research-analyst-agent
status: "addendum only — does not replace the named files' methodology, tagging schema, or quality controls"
---

# Perception Layer — Monthly Cadence Addendum

## Purpose
The five perception/validation agents listed above keep their full original methodology, source stacks, tagging schemas, and quality controls exactly as written in their respective SKILL files. Only operating cadence and batch volume change for the monthly format. This addendum is the single place that change is documented, rather than rewriting five files to say the same thing.

## What Changes

### Cadence
Weekly batch collection (originally "every Monday 00:00 UTC") is replaced with **continuous rolling collection** across the full 4–5 week production window, with two checkpoints:
- **Mid-window informal review (~T-14 days before publication):** light triage to surface early essay candidates and branch points; not a validation freeze.
- **Validation freeze (~T-10 days before publication):** Research Analyst Agent performs the full validation, scoring, and routing pass on the month's accumulated signal set. After this point, new signals are held for next month's window unless explicitly breaking (see Breaking Signal Triage, unchanged from original files).

### Volume
Monthly raw intake is roughly 4–5x weekly raw intake by construction (longer window). Research Analyst's noise-filtering target band (30–50% filtered as noise) is unchanged in percentage terms, but the editorial planning assumption for validated Medium-strength-or-higher signals feeding the eleven sections rises from ~10–15/week to a target band of **35–55 validated signals per monthly issue**. This is a planning guide for the human operator, not a hard quota — quality bar is unchanged.

### New Tagging Field
Add one optional field to the standard signal schema used by all five agents:
```json
"essay_candidate": true
```
Any agent may set this to `true` on a signal it believes could anchor a Deep Research Essay (see `SKILL_deep_research_essay_agent.md` topic-selection criteria). This field is reviewed at the T-14-day mid-window check by the Synthesis Agent.

## What Does Not Change
- Source tiering (Tier 1–5), confidence scoring, novelty flags: unchanged.
- Noise removal categories (content, source, relevance noise): unchanged.
- Routing logic (signal type → downstream agent): unchanged in mechanism; downstream agent names update per the new section-ownership map in `SKILL_monthly_editorial_architecture.md`.
- Escalation protocols to the human operator: unchanged.

## Updated Routing Table

| Old Destination (Weekly) | New Destination (Monthly) |
|---|---|
| Layer Specialist: Energy/Chips/Infrastructure | engineering-frontier-agent |
| Layer Specialist: Models | models-papers-repositories-agent |
| Layer Specialist: Applications | commercial-strategy-agent |
| Policy & Regulation Strategist | policy-geopolitics-strategist |
| Taleb Agent | scenarios-forecasts-agent (fragility-flavored scenarios) |
| Thiel Agent | scenarios-forecasts-agent (contrarian-flavored scenarios) |
| Synthesis Agent (Forward Look feature) | scenarios-forecasts-agent (scenario time horizons) + signals-metrics-agent (standing KPIs) |

## Quality Checklist
- [ ] Validation freeze occurs at T-10 days, not later — Deep Research Essay drafting depends on it being on time.
- [ ] essay_candidate flags reviewed at T-14 days, not lost in the general signal pool.
- [ ] Monthly validated-signal count logged against the 35–55 planning band; significant deviation (either direction) flagged to the operator as a coverage signal in itself.
