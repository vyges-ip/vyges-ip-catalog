#!/usr/bin/env python3
"""Validate every metadata/*.json against the bundled Vyges metadata schema and
emit a *report-only* drift summary.

This is a periodic signal, NOT a gate: the script always exits 0 so a scheduled
run never fails the build on drift. It complements sync_metadata.py — that one
mirrors the org into metadata/; this one tells you how far the mirrored corpus
has drifted from the published metadata schema.

Schema sourcing
───────────────
The catalog vendors a copy of the bundled schema at
    schema/vyges-metadata.schema.json
This is the simplest robust source: the schema's authoring repo is separate and
not always reachable from this repo's CI. Pass --schema to point elsewhere, or
set SCHEMA_URL to fetch a fresh copy at runtime (falls back to the vendored copy
on any failure).

Output
──────
  - DRIFT.md            committed/artifact report (counts per category + per-IP
                        failing list)
  - $GITHUB_STEP_SUMMARY (when set) — same report in the Actions job summary
  - stdout              short tally

Usage:
    python scripts/check_schema_drift.py --metadata-dir metadata \
        --schema schema/vyges-metadata.schema.json --report DRIFT.md
"""

from __future__ import annotations

import argparse
import datetime as dt
import glob
import json
import os
import sys
import urllib.request
from collections import Counter, defaultdict
from pathlib import Path
from typing import Dict, List, Tuple


def load_schema(schema_path: Path) -> dict:
    url = os.environ.get("SCHEMA_URL")
    if url:
        try:
            with urllib.request.urlopen(url, timeout=20) as resp:
                if resp.status == 200:
                    print(f"schema: fetched fresh copy from {url}")
                    return json.loads(resp.read())
        except Exception as e:  # noqa: BLE001
            print(f"schema: fetch from SCHEMA_URL failed ({e}); using vendored copy")
    return json.loads(schema_path.read_text())


def categorize(message: str) -> str:
    if "is not one of" in message:
        return "enum_violation"
    if "is not of type" in message:
        return "type_violation"
    if "is a required property" in message:
        return "missing_required"
    if "Additional properties" in message or "additionalProperties" in message:
        return "additional_property"
    if "do not match any of the regexes" in message:
        return "unknown_top_level_property"
    if "does not match" in message:
        return "pattern_violation"
    return "other"


def validate_corpus(schema: dict, files: List[Path]) -> Tuple[Dict[str, List[str]], Counter]:
    from jsonschema import Draft202012Validator  # local import keeps --help cheap

    validator = Draft202012Validator(schema)
    per_ip: Dict[str, List[str]] = {}
    categories: Counter = Counter()
    for f in files:
        try:
            data = json.loads(f.read_text())
        except Exception as e:  # noqa: BLE001
            per_ip[f.name] = [f"JSON parse error: {e}"]
            categories["parse_error"] += 1
            continue
        errs = sorted(validator.iter_errors(data), key=lambda e: list(map(str, e.absolute_path)))
        if not errs:
            continue
        msgs = []
        for e in errs:
            loc = "/".join(str(p) for p in e.absolute_path) or "<root>"
            msgs.append(f"[{loc}] {e.message}")
            categories[categorize(e.message)] += 1
        per_ip[f.name] = msgs
    return per_ip, categories


def render_report(total: int, per_ip: Dict[str, List[str]], categories: Counter) -> str:
    now = dt.datetime.now(dt.timezone.utc).replace(microsecond=0).isoformat()
    failing = len(per_ip)
    lines: List[str] = []
    lines.append("# Metadata schema drift report")
    lines.append("")
    lines.append(f"- **Generated:** {now}")
    lines.append(f"- **Schema:** bundled Vyges metadata schema (vendored at `schema/vyges-metadata.schema.json`)")
    lines.append(f"- **Total IP metadata files:** {total}")
    lines.append(f"- **Failing schema validation:** {failing}/{total}")
    lines.append(f"- **Passing:** {total - failing}/{total}")
    lines.append("")
    lines.append("> Report-only. This check never fails the build; it is a periodic drift signal.")
    lines.append("")
    lines.append("## Error counts by category")
    lines.append("")
    if categories:
        lines.append("| Category | Count |")
        lines.append("| --- | ---: |")
        for cat, n in categories.most_common():
            lines.append(f"| {cat} | {n} |")
    else:
        lines.append("No schema errors. The corpus matches the bundled schema.")
    lines.append("")
    if per_ip:
        lines.append("## Failing IPs")
        lines.append("")
        lines.append("| IP metadata file | Error count |")
        lines.append("| --- | ---: |")
        for name, msgs in sorted(per_ip.items(), key=lambda x: (-len(x[1]), x[0])):
            lines.append(f"| `{name}` | {len(msgs)} |")
        lines.append("")
        lines.append("<details><summary>Per-IP error detail</summary>")
        lines.append("")
        for name, msgs in sorted(per_ip.items(), key=lambda x: (-len(x[1]), x[0])):
            lines.append(f"### `{name}` ({len(msgs)})")
            lines.append("")
            for m in msgs:
                lines.append(f"- {m}")
            lines.append("")
        lines.append("</details>")
        lines.append("")
    return "\n".join(lines)


def main() -> int:
    ap = argparse.ArgumentParser(description="Report-only metadata schema drift check.")
    ap.add_argument("--metadata-dir", default="metadata")
    ap.add_argument("--schema", default="schema/vyges-metadata.schema.json")
    ap.add_argument("--report", default="DRIFT.md")
    args = ap.parse_args()

    schema_path = Path(args.schema)
    if not schema_path.exists() and not os.environ.get("SCHEMA_URL"):
        print(f"ERROR: schema not found at {schema_path} and SCHEMA_URL unset", file=sys.stderr)
        # still report-only — emit an empty report and exit 0
        Path(args.report).write_text("# Metadata schema drift report\n\nSchema unavailable — skipped.\n")
        return 0

    schema = load_schema(schema_path)
    files = [Path(p) for p in sorted(glob.glob(os.path.join(args.metadata_dir, "*.json")))]
    per_ip, categories = validate_corpus(schema, files)

    report = render_report(len(files), per_ip, categories)
    Path(args.report).write_text(report + "\n")

    step_summary = os.environ.get("GITHUB_STEP_SUMMARY")
    if step_summary:
        with open(step_summary, "a") as fh:
            fh.write(report + "\n")

    failing = len(per_ip)
    print(f"drift: {failing}/{len(files)} failing; categories={dict(categories.most_common())}")
    print(f"drift: report written to {args.report}")
    # report-only: never fail the build
    return 0


if __name__ == "__main__":
    sys.exit(main())
