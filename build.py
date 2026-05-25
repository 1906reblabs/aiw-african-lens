#!/usr/bin/env python3
"""
build.py — AI Weekly Lens · Build Orchestrator
===============================================
Single entry point for every build operation.

Usage
-----
  python build.py issue content/issues/aiw-026-12-content.md
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
"""

import sys
import argparse
from pathlib import Path
from jinja2 import Environment, FileSystemLoader

from afi_parser import parse_issue, parse_registry, output_path_for


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


def _render_issue(content_path: Path, out_dir: Path,
                  env: Environment, force: bool) -> None:
    out = output_path_for(content_path, out_dir / "weekly")
    if not force and not _is_stale(content_path, out):
        print(f"  –  {out.name}  (up to date)")
        return
    ctx  = parse_issue(content_path)
    html = env.get_template("issue.j2").render(e=ctx)
    _write(html, out)
    print(f"  ✓  {out}  ({out.stat().st_size / 1024:.1f} KB)")


def _render_index(registry_path: Path, out_dir: Path,
                  env: Environment, force: bool) -> None:
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

    # ── Weekly index ────────────────────────────────────────────────────────
    out_wkly = out_dir / "weekly" / "index.html"
    if force or _is_stale(registry_path, out_wkly):
        html = tmpl.render(page_mode="weekly", **ctx)
        _write(html, out_wkly)
        print(f"  ✓  {out_wkly}  ({out_wkly.stat().st_size / 1024:.1f} KB)")
    else:
        print(f"  –  weekly/{out_wkly.name}  (up to date)")


# ── Commands ──────────────────────────────────────────────────────────────────
def cmd_issue(args) -> None:
    env = _env(args.tmpl)
    for cf in args.content_file:
        _render_issue(Path(cf), Path(args.out), env, args.force)


def cmd_index(args) -> None:
    env = _env(args.tmpl)
    _render_index(Path(args.registry), Path(args.out), env, args.force)


def cmd_all(args) -> None:
    env      = _env(args.tmpl)
    out_dir  = Path(args.out)
    reg_path = Path(args.registry)

    # Discover every content file
    issues_dir = Path("content/issues")
    content_files = sorted(issues_dir.glob("*-content.md")) if issues_dir.exists() else []

    print(f"\nBuilding all  ({len(content_files)} issues + 2 indexes)\n")

    for cf in content_files:
        _render_issue(cf, out_dir, env, args.force)

    print()
    _render_index(reg_path, out_dir, env, args.force)
    print()


# ── CLI ───────────────────────────────────────────────────────────────────────
def main() -> None:
    root = Path(__file__).parent

    p = argparse.ArgumentParser(
        prog="build.py",
        description="AI Weekly Lens build orchestrator",
    )
    p.add_argument("--out",      default=str(root / "docs"),            metavar="DIR")
    p.add_argument("--registry", default=str(root / "content/registry.yaml"), metavar="FILE")
    p.add_argument("--tmpl",     default=str(root / "templates"),       metavar="DIR")
    p.add_argument("--force",    action="store_true",
                   help="Rebuild even when output is newer than source")

    sub = p.add_subparsers(dest="command", required=True)

    # issue
    p_issue = sub.add_parser("issue", help="Build one edition from a content file")
    p_issue.add_argument("content_file", nargs="+", metavar="CONTENT_FILE")
    p_issue.add_argument("--force", action="store_true")
    p_issue.set_defaults(func=cmd_issue)

    # index
    p_index = sub.add_parser("index", help="Rebuild both index pages from registry")
    p_index.add_argument("--force", action="store_true")
    p_index.set_defaults(func=cmd_index)

    # all
    p_all = sub.add_parser("all", help="Build all issues + both indexes")
    p_all.add_argument("--force", action="store_true")
    p_all.set_defaults(func=cmd_all)

    args = p.parse_args()
    args.func(args)


if __name__ == "__main__":
    main()
