#!/usr/bin/env python3
"""
build.py — AIW African Lens · Build Orchestrator
===================================================
Single entry point for every build operation.

Usage
-----
  python build.py issue content/issues/aiw-2026-07-content.md
  python build.py index
  python build.py all
  python build.py all --force

Commands
--------
  issue <content_file>   Build one edition HTML from a content .md file
  index                  Rebuild both index pages from the registry
  all                    Build every issue + both indexes (skips stale by default)

Options
-------
  --force     Rebuild even when output is newer than source
  --out DIR   Override output root directory (default: docs)
  --registry  Override registry path (default: content/registry.yaml)
  --tmpl DIR  Override templates directory (default: templates)

Format routing
--------------
Each content file's schema is auto-detected (see afi_parser.peek_format):
  • v2 (Monthly, AIW-YYYY-MM)  → rendered via templates/issue.j2, written to
    <out>/monthly/<edition>.html, with a build-time word-count QA line printed
    against the 10,600–16,200 target band.
  • v1 (legacy Weekly, AIW-026-NN) → NOT rendered under this pipeline.
    issue.j2 only supports the eleven-section Monthly schema. v1 files are
    reported and skipped so `build.py all` does not fail partway through a
    mixed Volume I / Volume II content directory. See
    MIGRATION_NOTES_weekly_to_monthly.md.
"""

import sys
import argparse
from pathlib import Path
from jinja2 import Environment, FileSystemLoader

from afi_parser import parse_issue, parse_registry, output_path_for, peek_format


# ── Jinja2 environment factory ────────────────────────────────────────────────
def _env(template_dir: Path) -> Environment:
    return Environment(
        loader=FileSystemLoader(str(template_dir)),
        autoescape=False,
        trim_blocks=True,
        lstrip_blocks=True,
    )


# ── Stale check ───────────────────────────────────────────────────────────────
def _is_stale(src: Path, out: Path) -> bool:
    """Return True if output is missing or older than source."""
    return not out.exists() or src.stat().st_mtime > out.stat().st_mtime


# ── Render helpers ────────────────────────────────────────────────────────────
def _write(html: str, out: Path) -> None:
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(html, encoding="utf-8")


def _render_issue(content_path: Path, out_dir: Path, env: Environment, force: bool) -> None:
    fmt = peek_format(content_path)

    if fmt == "v1":
        out = output_path_for(content_path, out_dir / "weekly")
        print(f"  ⊘  {content_path.name}  (legacy v1/weekly format — not rendered under "
              f"the v2 pipeline; archived output assumed already built at {out}. "
              f"See MIGRATION_NOTES_weekly_to_monthly.md.)")
        return

    out = output_path_for(content_path, out_dir / "monthly")
    if not force and not _is_stale(content_path, out):
        print(f"  –  {out.name}  (up to date)")
        return

    ctx = parse_issue(content_path)
    html = env.get_template("issue.j2").render(e=ctx)
    _write(html, out)

    wc = ctx.get("word_count_report", {})
    flag = "" if wc.get("status") == "within target" else f"  ⚠ {wc.get('status', '')}"
    print(f"  ✓  {out}  ({out.stat().st_size / 1024:.1f} KB) — "
          f"~{wc.get('total', '?')} words "
          f"[{wc.get('target_low', '?')}–{wc.get('target_high', '?')} target]{flag}")


def _render_index(registry_path: Path, out_dir: Path, env: Environment, force: bool) -> None:
    ctx = parse_registry(registry_path)
    tmpl = env.get_template("index.j2")

    # ── Main archive index ──────────────────────────────────────────────────
    out_main = out_dir / "index.html"
    if force or _is_stale(registry_path, out_main):
        html = tmpl.render(page_mode="archive", **ctx)
        _write(html, out_main)
        print(f"  ✓  {out_main}  ({out_main.stat().st_size / 1024:.1f} KB)")
    else:
        print(f"  –  {out_main.name}  (up to date)")

    # ── Weekly index (Volume I archive — unchanged) ─────────────────────────
    out_wkly = out_dir / "weekly" / "index.html"
    if force or _is_stale(registry_path, out_wkly):
        html = tmpl.render(page_mode="weekly", **ctx)
        _write(html, out_wkly)
        print(f"  ✓  {out_wkly}  ({out_wkly.stat().st_size / 1024:.1f} KB)")
    else:
        print(f"  –  weekly/{out_wkly.name}  (up to date)")

    # ── Monthly index (Volume II — requires a monthly-aware index.j2; see
    #    README_v2_monthly.md "Required Engineering Changes" if this template
    #    mode does not yet exist) ──────────────────────────────────────────
    out_mthly = out_dir / "monthly" / "index.html"
    if force or _is_stale(registry_path, out_mthly):
        try:
            html = tmpl.render(page_mode="monthly", **ctx)
            _write(html, out_mthly)
            print(f"  ✓  {out_mthly}  ({out_mthly.stat().st_size / 1024:.1f} KB)")
        except Exception as exc:
            print(f"  ⊘  monthly/index.html  (skipped — index.j2 does not yet support "
                  f"page_mode='monthly': {exc})")
    else:
        print(f"  –  monthly/{out_mthly.name}  (up to date)")


# ── Commands ──────────────────────────────────────────────────────────────────
def cmd_issue(args) -> None:
    env = _env(Path(args.tmpl))
    for cf in args.content_file:
        _render_issue(Path(cf), Path(args.out), env, args.force)


def cmd_index(args) -> None:
    env = _env(Path(args.tmpl))
    _render_index(Path(args.registry), Path(args.out), env, args.force)


def cmd_all(args) -> None:
    env = _env(Path(args.tmpl))
    out_dir = Path(args.out)
    reg_path = Path(args.registry)

    # Discover every content file (Volume I + Volume II both live under
    # content/issues/ with the *-content.md suffix; format is auto-detected
    # per file, so no separate directory split is required).
    issues_dir = Path("content/issues")
    content_files = sorted(issues_dir.glob("*-content.md")) if issues_dir.exists() else []

    print(f"\nBuilding all  ({len(content_files)} content files found + indexes)\n")

    rendered, skipped = 0, 0
    for cf in content_files:
        before = sys.stdout
        _render_issue(cf, out_dir, env, args.force)
        if peek_format(cf) == "v1":
            skipped += 1
        else:
            rendered += 1

    print()
    _render_index(reg_path, out_dir, env, args.force)
    print(f"\n{rendered} Volume II (monthly) issue(s) processed, "
          f"{skipped} Volume I (legacy weekly) issue(s) skipped.\n")


# ── CLI ───────────────────────────────────────────────────────────────────────
def main() -> None:
    root = Path(__file__).parent

    p = argparse.ArgumentParser(
        prog="build.py",
        description="AIW African Lens build orchestrator",
    )
    p.add_argument("--out", default=str(root / "docs"), metavar="DIR")
    p.add_argument("--registry", default=str(root / "content/registry.yaml"), metavar="FILE")
    p.add_argument("--tmpl", default=str(root / "templates"), metavar="DIR")
    p.add_argument("--force", action="store_true",
                    help="Rebuild even when output is newer than source")

    sub = p.add_subparsers(dest="command", required=True)

    # issue
    p_issue = sub.add_parser("issue", help="Build one edition from a content file")
    p_issue.add_argument("content_file", nargs="+", metavar="CONTENT_FILE")
    p_issue.add_argument("--force", action="store_true")
    p_issue.set_defaults(func=cmd_issue)

    # index
    p_index = sub.add_parser("index", help="Rebuild index pages from the registry")
    p_index.add_argument("--force", action="store_true")
    p_index.set_defaults(func=cmd_index)

    # all
    p_all = sub.add_parser("all", help="Build all issues + indexes")
    p_all.add_argument("--force", action="store_true")
    p_all.set_defaults(func=cmd_all)

    args = p.parse_args()
    args.func(args)


if __name__ == "__main__":
    main()
