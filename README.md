# AI Weekly African Lens

**Institutional-grade intelligence tracking Africa's AI stack across 54 nations.**

Published every Tuesday at 06:00 SAST · Hosted at [simphiwemlotshwa.substack.com](https://simphiwemlotshwa.substack.com/) · Deployed via GitHub Pages

---

## What This Is

AI Weekly African Lens is a weekly intelligence publication covering artificial intelligence, machine learning, and data science developments across all 54 African Union member states. Each edition ranks 10 developments by strategic importance, applies first/second/third-order analysis across Africa's five-layer AI stack, and delivers fragility assessments, contrarian bets, country spotlights, and a forward events calendar.

The publication does not aggregate news. It produces intelligence — analysis that changes how a sophisticated reader thinks or acts, not a summary of what happened.

**Current archive:** AIW-026-01 through AIW-026-12 · March–May 2026

---

## Repository Structure

```
aiw-african-lens/
│
├── content/
│   ├── issues/                  # Per-edition content files (YAML frontmatter)
│   │   ├── aiw-026-12-content.md
│   │   ├── aiw-026-11-content.md
│   │   └── ...
│   └── registry.yaml            # Master editions index — source of truth for all index pages
│
├── templates/
│   ├── issue.j2                 # Jinja2 template for individual edition HTML
│   └── index.j2                 # Jinja2 template for archive and weekly index pages
│
├── docs/                        # Built output — served by GitHub Pages
│   ├── index.html               # Root archive index
│   ├── weekly/
│   │   ├── index.html           # Weekly editions index
│   │   ├── aiw-026-12.html
│   │   └── ...
│   └── editions/                # Daily editions (hand-authored)
│
├── afi_parser.py                # Content parser — YAML → template context
├── build.py                     # Build orchestrator
├── requirements.txt
└── .github/workflows/build.yml  # CI: auto-build and deploy on push to main
```

---

## The Build Pipeline

Content is authored as structured YAML-frontmatter Markdown files. The build system separates editorial intelligence from HTML construction.

```
aiw-026-12-content.md          (editorial — structured YAML + Markdown prose)
        ↓  afi_parser.py
Template context dict           (Python — validates, processes, converts MD → HTML)
        ↓  Jinja2
aiw-026-12.html                 (output — publication-ready HTML)
        ↓  GitHub Pages
Live at /weekly/aiw-026-12.html
```

### Build Commands

```bash
# Build a single edition
python build.py issue content/issues/aiw-026-12-content.md

# Rebuild both index pages from the registry
python build.py index

# Build everything (stale-check by default)
python build.py all

# Force rebuild everything regardless of timestamps
python build.py all --force

# Override output directory
python build.py all --out /custom/output/dir
```

### Installation

```bash
git clone https://github.com/1906reblabs/aiw-african-lens.git
cd aiw-african-lens
pip install -r requirements.txt
python build.py all
```

**Python 3.11+ required.** Dependencies: `jinja2`, `pyyaml`, `markdown`.

---

## Publishing a New Edition

### Step 1 — Author the content file

Create `content/issues/aiw-026-XX-content.md` using the YAML-frontmatter schema. Copy the most recent edition as your template. Required top-level fields:

```yaml
---
edition_id: AIW-026-XX
date: "DD Month YYYY"
window_start: "DD Month"
window_end: "DD Month YYYY"
title: "Edition Title"
title_sub: "Edition Subtitle"
deck: >
  150-word teaser paragraph.
developments_count: 10
nations_covered: N
prev_edition: aiw-026-NN.html
prev_edition_id: AIW-026-NN
next_edition: ""
---
```

Full schema documentation: see any existing `*-content.md` file in `content/issues/`.

### Step 2 — Update the registry

In `content/registry.yaml`:

1. Copy the most recent `weekly:` list entry
2. Paste it at the **top** of the list (above the previous entry)
3. Update all fields for the new edition
4. Set `status: "new"` and `badge: "gold"` on the new entry
5. Change the previous top entry to `status: "available"` and `badge: "teal"`
6. Increment `stats.weekly_total` by 1

### Step 3 — Build and verify

```bash
python build.py issue content/issues/aiw-026-XX-content.md
python build.py index
```

Open `docs/weekly/aiw-026-XX.html` and `docs/index.html` in a browser to verify rendering.

### Step 4 — Commit and push

```bash
git add content/ docs/
git commit -m "publish: AIW-026-XX — Edition Title"
git push origin main
```

The GitHub Actions workflow (`build.yml`) runs automatically on push to `main` and rebuilds all HTML from source, committing the output to `docs/`. GitHub Pages serves from `docs/`.

---

## Content Schema Reference

Each edition content file is structured YAML with Markdown prose in multi-line string fields. The parser (`afi_parser.py`) converts all prose fields to HTML before handing the context to Jinja2.

### Top-5 Signals

```yaml
signals:
  - rank: 1
    title: "Signal headline"
    tags:
      - label: "Policy"
        css: "tag-policy"     # tag-policy | tag-infra | tag-geo | tag-tech |
                               # tag-security | tag-ecosystem | tag-research | tag-capital
    body: |
      Two paragraphs of factual description. No interpretation.
    analysis_1: >
      1st order — what literally changed. One sentence.
    analysis_2: >
      2nd order — the non-obvious implication. Rewrite if a smart reader
      could infer this in five seconds.
    analysis_3: >
      3rd order — what must investors, policymakers, or builders reconsider.
      Must produce a concrete strategic implication.
```

### Layer Analyses

```yaml
layers:
  - symbol: "⚡"         # ⚡ 🧱 🌐 🧠 🚀
    number: "1"
    name: "Energy"
    signal_count: "2 signals"
    highlight: "Short callout headline"
    body: |
      150–200 words of layer analysis prose.
```

### Fragility Index

```yaml
fragility_items:
  - frag_id: "FRAG-026-XX-01"
    domain: "Regulatory · Country"
    impact: "Severe"               # Severe | Moderate | Minor
    impact_css: "impact-high"      # impact-high | prob-med | ""
    probability: "Medium"
    prob_css: "prob-med"
    horizon: "6–12 months"
    title: "Fragility headline"
    body: |
      Description of the fragility. Precise actors, specific conditions.
      No vague language.
    mitigation: |
      Concrete mitigation path. Must be actionable.
```

### Contrarian Bets

```yaml
contrarian_items:
  - cb_id: "CB-026-XX-01"
    cb_type: "Overlooked Country · Long-Term"
    consensus: >
      What everyone currently believes.
    position_head: "The contrarian claim headline"
    position_body: |
      The argument. Must include mechanism for why the consensus is wrong.
    evidence: >
      Specific signals supporting the contrarian view.
    falsification: >
      What would make this position wrong. Prevents ideological lock-in.
```

---

## The Five-Layer AI Stack

All analysis is referenced against Africa's AI stack:

| # | Symbol | Layer | Domain |
|---|--------|-------|--------|
| 1 | ⚡ | Energy | Power generation, grid reliability, renewable energy for compute |
| 2 | 🧱 | Chips | Semiconductors, GPU access, export controls, compute hardware |
| 3 | 🌐 | Infrastructure | Data centres, connectivity, subsea cables, cloud regions |
| 4 | 🧠 | Models | AI model development, NLP/CV research, foundation models |
| 5 | 🚀 | Applications | AI products, sector deployments, commercial traction |

---

## Editorial Standards

**Voice:** Senior intelligence analyst. Not journalist, not academic, not marketer.

**Default output:** Insight, not news. Every claim must answer: does this change how a sophisticated reader thinks or acts?

**Three-tier analysis standard — mandatory for all signal analysis:**
- 🔵 **1st Order** — What literally happened? (floor, not ceiling)
- 🟡 **2nd Order** — What non-obvious implication does this create?
- 🔴 **3rd Order** — What must investors, policymakers, or builders now reconsider?

**Banned phrases:** leapfrog · African lion · the next Silicon Valley · powering Africa's AI revolution · on the continent *(as opener)* · it remains to be seen · in recent years · increasingly

**Country coverage:** Editions rotate country spotlight beyond the Nigeria-Kenya-South Africa default axis. Anglophone capital-city bias is the most common failure mode in African tech coverage.

**Policy vs. deployment:** A government announcing an AI strategy and a government implementing one are entirely different signals. Never conflate them.

---

## The Agent Framework

Each edition is produced through a multi-agent intelligence pipeline:

| Agent | Role |
|-------|------|
| **Geo Scraper** | 54-country signal collection across all six African regional blocs |
| **Policy & Regulation Agent** | Legislative and governance signal collection |
| **Research Harvester** | Academic, lab, and conference signal collection |
| **Startup & Capital Tracker** | Funding rounds, acquisitions, market entry/exit |
| **Infra Signals Agent** | Energy, chips, connectivity, data centre signals |
| **Research Analyst Agent** | Signal validation, scoring, noise removal, routing |
| **Layer Specialists (×5)** | 1st/2nd/3rd order analysis per AI stack layer |
| **Policy Strategist** | Regulatory deep analysis, convergence tracking |
| **Taleb Agent** | Fragility Engine — finds what everyone else is not looking for |
| **Thiel Agent** | Contrarian Engine — finds what the consensus is missing |
| **Synthesis Agent** | Editor-in-Chief AI — assembles the final publication-ready report |

Full agent skill files are maintained in the editorial project repository.

---

## Archive

| Edition | Window | Theme | Status |
|---------|--------|-------|--------|
| AIW-026-12 | 19–25 May 2026 | The Governance Quality Audit | New |
| AIW-026-11 | 12–18 May 2026 | Before the Hearings | Available |
| AIW-026-10 | 05–11 May 2026 | The Consultation Week | Available |
| AIW-026-09 | 28 Apr–04 May 2026 | The Deployment Quarter | Available |
| AIW-026-08 | 21–27 Apr 2026 | The Post-GITEX Reckoning | Available |
| AIW-026-07 | 14–21 Apr 2026 | The Policy Moment Arrives | Available |
| AIW-026-06 | 08–14 Apr 2026 | South Africa's AI Policy Lands | Available |
| AIW-026-05 | 31 Mar–07 Apr 2026 | Infrastructure Ahead of Governance | Available |
| AIW-026-04 | 24–31 Mar 2026 | The Week Everything Converged | Coming Soon |
| AIW-026-03 | 17–24 Mar 2026 | The Sovereignty Inflection | Available |
| AIW-026-02 | 10–17 Mar 2026 | Governance Week | Coming Soon |
| AIW-026-01 | 03–10 Mar 2026 | Launch Week | Coming Soon |

---

## Deployment

The repository uses GitHub Pages served from the `docs/` directory on `main`. The GitHub Actions workflow (`.github/workflows/build.yml`) triggers on any push to `main` that touches `content/`, `templates/`, `afi_parser.py`, or `build.py` — rebuilding all HTML and committing the output automatically.

Manual rebuilds can be triggered via the GitHub Actions UI using the `workflow_dispatch` event.

---

## Subscribe

New editions published every Tuesday at 06:00 SAST.

**Substack:** [simphiwemlotshwa.substack.com](https://simphiwemlotshwa.substack.com/)

---

*AI Weekly African Lens — Intelligence, not aggregation.*  
*© 2026 The Weekly African Lens · 54 Nations · Q1–Q2 2026 Coverage*
