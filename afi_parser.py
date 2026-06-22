"""
afi_parser.py — AIW African Lens · Content Parser
====================================================
Parses YAML-frontmatter content files and the editions registry, returning
fully-processed Jinja2 template contexts.

Supports two schema generations:
  • v2 (current)  — the eleven-section Monthly Intelligence Review format
                    (Volume II, AIW-YYYY-MM editions, from AIW-2026-07 onward).
                    Detected by the presence of top-level `thesis` +
                    `executive_brief` keys.
  • v1 (legacy)   — the nine-section Weekly format (Volume I, AIW-026-NN
                    editions, AIW-026-01 through AIW-026-13). Detected by the
                    presence of a top-level `signals` key. Retained verbatim
                    for archival reference; build.py does not render v1
                    issues under the v2 pipeline (see
                    MIGRATION_NOTES_weekly_to_monthly.md).

Public API
----------
  parse_issue(path)       → dict   full processed context (v2 or v1)
  peek_format(path)       → str    'v2' | 'v1' — cheap format check, no field processing
  parse_registry(path)    → dict   context for templates/index.j2
  output_path_for(...)    → Path   derives docs/ output path from a content path
  word_count_report(ctx)  → dict   QA helper: rendered word count vs. target band
"""

import re
import yaml
import markdown as _md_lib
from pathlib import Path

# ── Markdown engine ────────────────────────────────────────────────────────────
_engine = _md_lib.Markdown(extensions=["nl2br"])


def _md(text) -> str:
    """Convert a markdown string to an HTML fragment."""
    if not text:
        return ""
    _engine.reset()
    return _engine.convert(str(text).strip())


def _s(value) -> str:
    """Coerce a YAML scalar to a stripped string, tolerating None."""
    return str(value).strip() if value is not None else ""


def _word_count_html(html) -> int:
    """Approximate the word count of an HTML fragment (strip tags, split on whitespace)."""
    if not html:
        return 0
    text = re.sub(r"<[^>]+>", " ", str(html))
    return len(text.split())


# ── YAML frontmatter extractor ─────────────────────────────────────────────────
def _load_yaml(path) -> dict:
    """Return parsed YAML from a file that is either pure YAML or has --- fences."""
    text = Path(path).read_text(encoding="utf-8")
    match = re.match(r"^---\s*\n(.*?)\n---\s*", text, re.DOTALL)
    if match:
        return yaml.safe_load(match.group(1))
    # Plain YAML file (no frontmatter fences — used for registry.yaml)
    return yaml.safe_load(text)


# ── Format detection ────────────────────────────────────────────────────────────
def _detect_format(data: dict) -> str:
    """
    'v2' for the eleven-section Monthly format, 'v1' for the legacy nine-section
    Weekly format. Detection uses mutually exclusive marker keys rather than an
    explicit version field, so existing Volume I content files do not need to be
    retroactively edited to keep working.
    """
    if "thesis" in data and "executive_brief" in data:
        return "v2"
    if "signals" in data:
        return "v1"
    raise ValueError(
        "Could not detect content schema for this file — expected either a "
        "'thesis' + 'executive_brief' key (v2/monthly) or a 'signals' key "
        "(v1/weekly legacy). Got top-level keys: " + ", ".join(data.keys())
    )


def peek_format(path) -> str:
    """
    Load just enough of a content file to detect its schema version without
    running the full field-processing pipeline. Cheap to call before deciding
    whether a stale-check / full parse is needed (see build.py).
    """
    return _detect_format(_load_yaml(path))


# ════════════════════════════════════════════════════════════════════════════
# v2 — MONTHLY FORMAT (current)
# ════════════════════════════════════════════════════════════════════════════

def _process_thesis(thesis: dict) -> dict:
    thesis = dict(thesis or {})
    thesis["statement_html"] = _md(thesis.get("statement", ""))
    thesis["evidence_html"] = _md(thesis.get("evidence", ""))
    thesis["implications_html"] = _md(thesis.get("implications", ""))
    thesis["falsification"] = _s(thesis.get("falsification", ""))
    thesis["last_month_verdict"] = _s(thesis.get("last_month_verdict", ""))
    thesis["last_month_verdict_text"] = _s(thesis.get("last_month_verdict_text", ""))

    verdict_key = thesis["last_month_verdict"].lower().split()[0] if thesis["last_month_verdict"] else "na"
    thesis["verdict_css"] = {
        "confirmed": "verdict-confirmed",
        "revised": "verdict-revised",
        "abandoned": "verdict-abandoned",
    }.get(verdict_key, "verdict-na")
    return thesis


def _process_executive_brief(eb: dict) -> dict:
    # NOTE: the processed list is stored under "briefs", not "items" — Jinja2's
    # dot-notation tries getattr() before dict lookup, and dict.items is a real
    # bound method, so `e.executive_brief.items` would silently return the
    # built-in method instead of this data. Same reasoning applies throughout
    # this module to any field that collides with dict.keys/values/get/etc.
    eb = dict(eb or {})
    briefs = []
    for item in eb.get("items", []):
        item = dict(item)
        item["headline"] = _s(item.get("headline", ""))
        item["what_happened"] = _s(item.get("what_happened", ""))
        item["why_it_matters"] = _s(item.get("why_it_matters", ""))
        item["watch"] = _s(item.get("watch", ""))
        briefs.append(item)
    eb["briefs"] = briefs

    notm = dict(eb.get("number_of_month", {}) or {})
    notm["label"] = _s(notm.get("label", ""))
    notm["value"] = _s(notm.get("value", ""))
    notm["context"] = _s(notm.get("context", ""))
    eb["number_of_month"] = notm
    return eb


_TREND_MAP = {
    "up": ("▲", "trend-up"),
    "down": ("▼", "trend-down"),
    "flat": ("—", "trend-flat"),
    "steady": ("—", "trend-flat"),
}


def _process_signals_metrics(sm: dict) -> dict:
    sm = dict(sm or {})
    kpis = []
    for kpi in sm.get("kpis", []):
        kpi = dict(kpi)
        symbol, css = _TREND_MAP.get(_s(kpi.get("trend", "flat")).lower(), ("—", "trend-flat"))
        kpi["trend_symbol"] = symbol
        kpi["trend_css"] = css
        kpi["label"] = _s(kpi.get("label", ""))
        kpi["value"] = _s(kpi.get("value", ""))
        kpi["trailing_3mo_avg"] = _s(kpi.get("trailing_3mo_avg", ""))
        kpi["note"] = _s(kpi.get("note", ""))
        kpis.append(kpi)
    sm["kpis"] = kpis

    metrics = []
    for m in sm.get("metrics_of_month", []):
        m = dict(m)
        m["title"] = _s(m.get("title", ""))
        m["body_html"] = _md(m.get("body", ""))
        metrics.append(m)
    sm["metrics_of_month"] = metrics

    sm["coverage_note"] = _s(sm.get("coverage_note", ""))
    return sm


def _process_essays(essays: list) -> list:
    out = []
    for e in essays or []:
        e = dict(e)
        e["title"] = _s(e.get("title", ""))
        e["dek"] = _s(e.get("dek", ""))
        e["tags"] = e.get("tags", [])
        for key in ("hook", "context_stakes", "core_argument", "evidence_chain",
                    "counterargument", "strategic_implications"):
            e[f"{key}_html"] = _md(e.get(key, ""))
        e["falsification"] = _s(e.get("falsification", ""))

        word_total = 0
        for key in ("hook_html", "context_stakes_html", "core_argument_html",
                    "evidence_chain_html", "counterargument_html", "strategic_implications_html"):
            word_total += _word_count_html(e.get(key, ""))
        word_total += len(e["falsification"].split())
        e["word_count"] = word_total
        out.append(e)
    return out


def _process_engineering_frontier(ef: dict) -> dict:
    ef = dict(ef or {})
    for key in ("opening", "power", "compute", "connectivity"):
        ef[f"{key}_html"] = _md(ef.get(key, ""))
    ef["dependency_watch"] = _s(ef.get("dependency_watch", ""))
    return ef


def _process_commercial_strategy(cs: dict) -> dict:
    cs = dict(cs or {})
    for key in ("lead", "capital_flow_read", "competitive_structure", "for_operator"):
        cs[f"{key}_html"] = _md(cs.get(key, ""))
    return cs


def _process_policy_geopolitics(pg: dict) -> dict:
    pg = dict(pg or {})
    pg["lead_html"] = _md(pg.get("lead", ""))

    actors = []
    for a in pg.get("actor_map", []):
        a = dict(a)
        for key in ("actor", "instrument", "leverage", "degrees_of_freedom"):
            a[key] = _s(a.get(key, ""))
        actors.append(a)
    pg["actor_map"] = actors

    pg["convergence_rows"] = pg.get("convergence_rows", [])  # same shape as v1 convergence table
    pg["branch_points"] = [_s(b) for b in pg.get("branch_points", [])]
    return pg


def _process_builders(builders: list) -> list:
    out = []
    for b in builders or []:
        b = dict(b)
        for key in ("name", "role", "country", "layer", "flag_style", "sourcing"):
            b[key] = _s(b.get(key, ""))
        b["badges"] = b.get("badges", [])
        for key in ("who", "why_it_matters", "the_bet"):
            b[f"{key}_html"] = _md(b.get(key, ""))
        out.append(b)
    return out


def _process_models_papers_repos(mpr: dict) -> dict:
    mpr = dict(mpr or {})
    mpr["lead_html"] = _md(mpr.get("lead", ""))

    bb = dict(mpr.get("benchmark_board", {}) or {})
    bb["columns"] = bb.get("columns", [])
    rows = []
    for r in bb.get("rows", []):
        r = dict(r)
        r["language"] = _s(r.get("language", ""))
        r["cells"] = r.get("values", [])  # renamed from "values" — collides with dict.values()
        r["changed"] = bool(r.get("changed", False))
        rows.append(r)
    bb["rows"] = rows
    mpr["benchmark_board"] = bb
    mpr["benchmark_note_html"] = _md(mpr.get("benchmark_note", ""))

    repos = []
    for r in mpr.get("repository_health", []):
        r = dict(r)
        r["name"] = _s(r.get("name", ""))
        r["body_html"] = _md(r.get("body", ""))
        repos.append(r)
    mpr["repository_health"] = repos

    mpr["dark_zones"] = _s(mpr.get("dark_zones", ""))
    return mpr


_SCENARIO_TYPE_CSS = {
    "fragility": "scenario-fragility",
    "contrarian": "scenario-contrarian",
    "hybrid": "scenario-hybrid",
}

_PROB_CSS = {
    "low": "prob-low",
    "medium": "prob-medium",
    "high": "prob-high",
}


def _process_scenarios(sf: dict) -> dict:
    sf = dict(sf or {})
    scenarios = []
    for s in sf.get("scenarios", []):
        s = dict(s)
        s["name"] = _s(s.get("name", ""))
        s["type"] = _s(s.get("type", ""))
        s["type_css"] = _SCENARIO_TYPE_CSS.get(s["type"].lower(), "scenario-fragility")
        s["probability_band"] = _s(s.get("probability_band", ""))
        s["prob_css"] = _PROB_CSS.get(s["probability_band"].lower().split()[0]
                                      if s["probability_band"] else "medium", "prob-medium")
        s["time_horizon"] = _s(s.get("time_horizon", ""))
        s["trigger_conditions_html"] = _md(s.get("trigger_conditions", ""))
        s["stack_cascade_html"] = _md(s.get("stack_cascade", ""))

        ro = dict(s.get("response_options", {}) or {})
        s["response_options"] = {
            "investor_html": _md(ro.get("investor", "")),
            "policymaker_html": _md(ro.get("policymaker", "")),
            "builder_html": _md(ro.get("builder", "")),
        }
        s["early_indicators_html"] = _md(s.get("early_indicators", ""))
        scenarios.append(s)
    sf["scenarios"] = scenarios

    sf["watchlist_update"] = [_md(w) for w in sf.get("watchlist_update", [])]
    sf["resolved_this_month"] = [_md(r) for r in sf.get("resolved_this_month", [])]
    return sf


def _process_reading_list(items: list) -> list:
    out = []
    for it in items or []:
        it = dict(it)
        for key in ("title", "source", "date", "url"):
            it[key] = _s(it.get(key, ""))
        it["annotation_html"] = _md(it.get("annotation", ""))
        out.append(it)
    return out


# Sections whose word count counts toward the published total — maps to the
# 10,600–16,200 target band defined in SKILL_monthly_editorial_architecture.md.
_WORDCOUNT_TARGET = (10_600, 16_200)


def word_count_report(ctx: dict) -> dict:
    """
    Approximate the issue's total rendered word count by walking every
    processed field in a v2 context, and compare it against the publication's
    target band. Used by build.py to print a build-time QA line, operationalizing
    the Synthesis Agent's "total word count within target band" checklist item.
    """
    total = 0

    th = ctx.get("thesis", {})
    total += _word_count_html(th.get("statement_html", ""))
    total += _word_count_html(th.get("evidence_html", ""))
    total += _word_count_html(th.get("implications_html", ""))
    total += len(th.get("falsification", "").split())
    total += len(th.get("last_month_verdict_text", "").split())

    for item in ctx.get("executive_brief", {}).get("briefs", []):
        total += len(item.get("what_happened", "").split())
        total += len(item.get("why_it_matters", "").split())
        total += len(item.get("watch", "").split())

    sm = ctx.get("signals_metrics", {})
    for m in sm.get("metrics_of_month", []):
        total += _word_count_html(m.get("body_html", ""))
    for kpi in sm.get("kpis", []):
        total += len(kpi.get("note", "").split())

    for e in ctx.get("deep_research_essays", []):
        total += e.get("word_count", 0)

    ef = ctx.get("engineering_frontier", {})
    for key in ("opening_html", "power_html", "compute_html", "connectivity_html"):
        total += _word_count_html(ef.get(key, ""))

    cs = ctx.get("commercial_strategy", {})
    for key in ("lead_html", "capital_flow_read_html", "competitive_structure_html", "for_operator_html"):
        total += _word_count_html(cs.get(key, ""))

    pg = ctx.get("policy_geopolitics", {})
    total += _word_count_html(pg.get("lead_html", ""))
    for a in pg.get("actor_map", []):
        total += len(a.get("instrument", "").split())
        total += len(a.get("leverage", "").split())
        total += len(a.get("degrees_of_freedom", "").split())
    for b in pg.get("branch_points", []):
        total += len(b.split())

    for b in ctx.get("african_builders", []):
        for key in ("who_html", "why_it_matters_html", "the_bet_html"):
            total += _word_count_html(b.get(key, ""))

    mpr = ctx.get("models_papers_repos", {})
    total += _word_count_html(mpr.get("lead_html", ""))
    total += _word_count_html(mpr.get("benchmark_note_html", ""))
    for r in mpr.get("repository_health", []):
        total += _word_count_html(r.get("body_html", ""))
    total += len(mpr.get("dark_zones", "").split())

    sf = ctx.get("scenarios_forecasts", {})
    for s in sf.get("scenarios", []):
        total += _word_count_html(s.get("trigger_conditions_html", ""))
        total += _word_count_html(s.get("stack_cascade_html", ""))
        ro = s.get("response_options", {})
        total += _word_count_html(ro.get("investor_html", ""))
        total += _word_count_html(ro.get("policymaker_html", ""))
        total += _word_count_html(ro.get("builder_html", ""))
        total += _word_count_html(s.get("early_indicators_html", ""))
    for w in sf.get("watchlist_update", []):
        total += _word_count_html(w)
    for r in sf.get("resolved_this_month", []):
        total += _word_count_html(r)

    for it in ctx.get("reading_list", []):
        total += _word_count_html(it.get("annotation_html", ""))

    total += _word_count_html(ctx.get("editorial_note_html", ""))

    low, high = _WORDCOUNT_TARGET
    if total < low:
        status = "below target"
    elif total > high:
        status = "above target"
    else:
        status = "within target"

    return {"total": total, "target_low": low, "target_high": high, "status": status}


def _parse_issue_v2(data: dict) -> dict:
    """Field processing for the eleven-section Monthly format."""
    data["_format_version"] = "v2"

    for key in ("deck", "editorial_note"):
        data[key] = _s(data.get(key, ""))
    data["editorial_note_html"] = _md(data.get("editorial_note", ""))

    data["masthead_stats"] = data.get("masthead_stats", [])

    data["thesis"] = _process_thesis(data.get("thesis", {}))
    data["executive_brief"] = _process_executive_brief(data.get("executive_brief", {}))
    data["signals_metrics"] = _process_signals_metrics(data.get("signals_metrics", {}))
    data["deep_research_essays"] = _process_essays(data.get("deep_research_essays", []))
    data["engineering_frontier"] = _process_engineering_frontier(data.get("engineering_frontier", {}))
    data["commercial_strategy"] = _process_commercial_strategy(data.get("commercial_strategy", {}))
    data["policy_geopolitics"] = _process_policy_geopolitics(data.get("policy_geopolitics", {}))
    data["african_builders"] = _process_builders(data.get("african_builders", []))
    data["models_papers_repos"] = _process_models_papers_repos(data.get("models_papers_repos", {}))
    data["scenarios_forecasts"] = _process_scenarios(data.get("scenarios_forecasts", {}))
    data["reading_list"] = _process_reading_list(data.get("reading_list", []))

    data["word_count_report"] = word_count_report(data)
    return data


# ════════════════════════════════════════════════════════════════════════════
# v1 — WEEKLY FORMAT (legacy, Volume I, AIW-026-01 → AIW-026-13)
# Retained verbatim for archival reference. Not used by templates/issue.j2;
# kept so the Volume I archive remains reproducible from source if ever needed.
# ════════════════════════════════════════════════════════════════════════════

def _process_signals_v1(signals: list) -> list:
    for s in signals:
        s["rank_str"] = f"{s['rank']:02d}"
        s["body_html"] = _md(s.get("body", ""))
        for key in ("analysis_1", "analysis_2", "analysis_3"):
            s[key] = str(s.get(key, "")).strip()
    return signals


def _process_layers_v1(layers: list) -> list:
    for layer in layers:
        layer["body_html"] = _md(layer.get("body", ""))
    return layers


def _process_research_v1(data: dict) -> dict:
    for key in ("research_african", "research_global"):
        if key in data:
            data[key]["body_html"] = _md(data[key].get("body", ""))
    return data


def _process_fragility_v1(items: list) -> list:
    for f in items:
        f["body_html"] = _md(f.get("body", ""))
        f["mitigation_html"] = _md(f.get("mitigation", ""))
    return items


def _process_contrarian_v1(items: list) -> list:
    for c in items:
        c["position_body_html"] = _md(c.get("position_body", ""))
        c["evidence"] = str(c.get("evidence", "")).strip()
        c["falsification"] = str(c.get("falsification", "")).strip()
    return items


def _process_spotlights_v1(spots: list) -> list:
    for s in spots:
        s["state_of_play_html"] = _md(s.get("state_of_play", ""))
        s["what_changed_html"] = _md(s.get("what_changed", ""))
        s["outlook_html"] = _md(s.get("outlook", ""))
    return spots


def _parse_issue_v1_legacy(data: dict) -> dict:
    """Field processing for the legacy nine-section Weekly format (Volume I)."""
    data["_format_version"] = "v1"

    for key in ("deck", "editorial_note", "opening_frame", "policy_body_1", "policy_body_2"):
        data[key] = str(data.get(key, "")).strip()

    data["opening_frame_html"] = _md(data.get("opening_frame", ""))
    data["policy_body_1_html"] = _md(data.get("policy_body_1", ""))
    data["policy_body_2_html"] = _md(data.get("policy_body_2", ""))

    data["signals"] = _process_signals_v1(data.get("signals", []))
    data["layers"] = _process_layers_v1(data.get("layers", []))
    data = _process_research_v1(data)
    data["fragility_items"] = _process_fragility_v1(data.get("fragility_items", []))
    data["contrarian_items"] = _process_contrarian_v1(data.get("contrarian_items", []))
    data["spotlights"] = _process_spotlights_v1(data.get("spotlights", []))

    return data


# ── Public: parse a single issue content file ──────────────────────────────────
def parse_issue(path) -> dict:
    """
    Parse an issue content .md file and return a fully-processed template
    context dict. Format (v2 monthly / v1 legacy weekly) is auto-detected.

    v2 contexts are ready for templates/issue.j2.
    v1 contexts are returned for archival/reference purposes only — build.py
    does not render them under the v2 pipeline (see
    MIGRATION_NOTES_weekly_to_monthly.md).

    Parameters
    ----------
    path : str | Path
        Path to the YAML-frontmatter content file,
        e.g. content/issues/aiw-2026-07-content.md

    Returns
    -------
    dict
        Template-ready context, tagged with data['_format_version'] = 'v1' | 'v2'.
    """
    data = _load_yaml(path)
    fmt = _detect_format(data)
    if fmt == "v2":
        return _parse_issue_v2(data)
    return _parse_issue_v1_legacy(data)


# ── Public: parse the editions registry ───────────────────────────────────────
def parse_registry(path) -> dict:
    """
    Parse the editions registry YAML and return a template context dict
    ready for templates/index.j2.

    Adds a 'monthly' list alongside the existing 'weekly' and 'daily' lists
    (empty by default) so the registry schema is forward-compatible with
    Volume II entries without requiring an index.j2 rewrite to load correctly.
    Full monthly-aware index page rendering is a separate follow-up task — see
    README_v2_monthly.md, "Required Engineering Changes."

    Parameters
    ----------
    path : str | Path
        Path to the registry file, e.g. content/registry.yaml

    Returns
    -------
    dict with keys: site, stats, themes, weekly, monthly, daily
    """
    data = _load_yaml(path)

    for ed in data.get("weekly", []):
        ed["summary"] = str(ed.get("summary", "")).strip()
    for ed in data.get("monthly", []):
        ed["summary"] = str(ed.get("summary", "")).strip()

    return {
        "site": data["site"],
        "stats": data["stats"],
        "themes": data.get("themes", []),
        "weekly": data.get("weekly", []),
        "monthly": data.get("monthly", []),
        "daily": data.get("daily", []),
    }


# ── Utility: derive output path from content path ─────────────────────────────
def output_path_for(content_path, output_dir="docs/monthly") -> Path:
    """
    Derive the HTML output path from a content file path.

    content/issues/aiw-2026-07-content.md  →  docs/monthly/aiw-2026-07.html
    content/issues/aiw-026-13-content.md   →  docs/weekly/aiw-026-13.html  (if
        output_dir is overridden to "docs/weekly" by the caller — see build.py,
        which routes v1/legacy files to docs/weekly and v2 files to docs/monthly)
    """
    stem = Path(content_path).stem            # aiw-2026-07-content
    edition_id = stem.replace("-content", "")  # aiw-2026-07
    return Path(output_dir) / f"{edition_id}.html"
