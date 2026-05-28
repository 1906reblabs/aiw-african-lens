"""
afi_parser.py — AI Weekly Lens · Content Parser
================================================
Parses YAML-frontmatter content files and the editions registry,
returning fully-processed Jinja2 template contexts.

Public API
----------
  parse_issue(path)     → dict  context for templates/issue.j2
  parse_registry(path)  → dict  context for templates/index.j2
"""

import re
import yaml
import markdown as _md_lib
from pathlib import Path

# ── Markdown engine ────────────────────────────────────────────────────────────
_engine = _md_lib.Markdown(extensions=["nl2br"])


def _md(text: str) -> str:
    """Convert a markdown string to an HTML fragment."""
    if not text:
        return ""
    _engine.reset()
    return _engine.convert(str(text).strip())


# ── YAML frontmatter extractor ─────────────────────────────────────────────────
def _load_yaml(path: Path) -> dict:
    """Return parsed YAML from a file that is either pure YAML or has --- fences."""
    text = Path(path).read_text(encoding="utf-8")
    match = re.match(r"^---\s*\n(.*?)\n---\s*", text, re.DOTALL)
    if match:
        return yaml.safe_load(match.group(1))
    # Plain YAML file (no frontmatter fences — used for registry.yaml)
    return yaml.safe_load(text)


# ── Field processors ───────────────────────────────────────────────────────────
def _process_signals(signals: list) -> list:
    for s in signals:
        s["rank_str"]   = f"{s['rank']:02d}"
        s["body_html"]  = _md(s.get("body", ""))
        # analysis fields stay as plain text (rendered inline in template)
        for key in ("analysis_1", "analysis_2", "analysis_3"):
            s[key] = str(s.get(key, "")).strip()
    return signals


def _process_layers(layers: list) -> list:
    for layer in layers:
        layer["body_html"] = _md(layer.get("body", ""))
    return layers


def _process_research(data: dict) -> dict:
    for key in ("research_african", "research_global"):
        if key in data:
            data[key]["body_html"] = _md(data[key].get("body", ""))
    return data


def _process_fragility(items: list) -> list:
    for f in items:
        f["body_html"]       = _md(f.get("body", ""))
        f["mitigation_html"] = _md(f.get("mitigation", ""))
    return items


def _process_contrarian(items: list) -> list:
    for c in items:
        c["position_body_html"] = _md(c.get("position_body", ""))
        c["evidence"]           = str(c.get("evidence", "")).strip()
        c["falsification"]      = str(c.get("falsification", "")).strip()
    return items


def _process_spotlights(spots: list) -> list:
    for s in spots:
        s["state_of_play_html"] = _md(s.get("state_of_play", ""))
        s["what_changed_html"]  = _md(s.get("what_changed", ""))
        s["outlook_html"]       = _md(s.get("outlook", ""))
    return spots


# ── Public: parse a single issue content file ──────────────────────────────────
def parse_issue(path) -> dict:
    """
    Parse an issue content .md file and return a fully-processed
    template context dict ready for templates/issue.j2.

    Parameters
    ----------
    path : str | Path
        Path to the YAML-frontmatter content file
        e.g. content/issues/aiw-026-12-content.md

    Returns
    -------
    dict
        All fields with markdown bodies pre-converted to HTML.
        Pass directly as ``e=context`` to the Jinja2 template.
    """
    data = _load_yaml(path)

    # Scalar string normalisation
    for key in ("deck", "editorial_note", "opening_frame",
                "policy_body_1", "policy_body_2"):
        data[key] = str(data.get(key, "")).strip()

    # Prose → HTML
    data["opening_frame_html"]  = _md(data.get("opening_frame", ""))
    data["policy_body_1_html"]  = _md(data.get("policy_body_1", ""))
    data["policy_body_2_html"]  = _md(data.get("policy_body_2", ""))

    # Structured sections
    data["signals"]         = _process_signals(data.get("signals", []))
    data["layers"]          = _process_layers(data.get("layers", []))
    data                    = _process_research(data)
    data["fragility_items"] = _process_fragility(data.get("fragility_items", []))
    data["contrarian_items"]= _process_contrarian(data.get("contrarian_items", []))
    data["spotlights"]      = _process_spotlights(data.get("spotlights", []))

    return data


# ── Public: parse the editions registry ───────────────────────────────────────
def parse_registry(path) -> dict:
    """
    Parse the editions registry YAML and return a template context dict
    ready for templates/index.j2 (both archive and weekly index modes).

    Parameters
    ----------
    path : str | Path
        Path to the registry file, e.g. content/registry.yaml

    Returns
    -------
    dict with keys: site, stats, themes, weekly, daily
    """
    data = _load_yaml(path)

    # Guard: if the registry YAML was saved as a bare list of editions
    # (missing the top-level site/stats/themes/weekly/daily wrapper),
    # reconstruct the expected dict so the build does not crash.
    if isinstance(data, list):
        data = {
            "site": {
                "brand":    "The Weekly African Lens",
                "substack": "https://simphiwemlotshwa.substack.com/",
                "coverage": "Q1-Q2",
                "nations":  54,
            },
            "stats": {
                "daily_editions":     "21+",
                "weekly_total":       len(data),
                "developments_ranked": "110+",
            },
            "themes": [],
            "weekly": data,
            "daily":  [],
        }

    # Normalise weekly summaries to plain strings
    for ed in data.get("weekly", []):
        ed["summary"] = str(ed.get("summary", "")).strip()

    return {
        "site":   data["site"],
        "stats":  data["stats"],
        "themes": data.get("themes", []),
        "weekly": data["weekly"],
        "daily":  data.get("daily", []),
    }


# ── Utility: derive output path from content path ─────────────────────────────
def output_path_for(content_path, output_dir="docs/weekly") -> Path:
    """
    Derive the HTML output path from a content file path.

    content/issues/aiw-026-12-content.md  →  docs/weekly/aiw-026-12.html
    """
    stem = Path(content_path).stem          # aiw-026-12-content
    edition_id = stem.replace("-content", "")  # aiw-026-12
    return Path(output_dir) / f"{edition_id}.html"
