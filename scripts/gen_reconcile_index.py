#!/usr/bin/env python3
"""Catalog-wide metadata<->RTL reconcile index.

The schema-drift report (check_schema_drift.py) answers "does each IP's metadata
match the *schema*". This answers the complementary question — "does each IP's
metadata still match its *RTL*" — across the whole catalog, by running the
`vyges metadata reconcile` binary against every IP that ships RTL.

Unlike schema-drift (metadata-only), reconcile needs the RTL, so this consumes a
directory of IP *checkouts* (each subdir an IP with rtl/ + vyges-metadata.json) —
the CI workflow clones them. For each IP it runs:

    vyges metadata reconcile <ip-dir> --json

and aggregates the gap/drift counts into:
  - reconcile-index.json  (per-IP gap/drift counts + a catalog summary)
  - RECONCILE.md          (human-readable report, like DRIFT.md)

Report-only: a periodic health signal. Per-repo gating is the IP repo's own
`metadata-check` workflow (reusable-metadata-check.yml).

Usage:
  python scripts/gen_reconcile_index.py --ips-dir <checkouts> \
      --bin "vyges metadata" --index reconcile-index.json --report RECONCILE.md
"""

import argparse
import json
import shlex
import subprocess
import sys
from pathlib import Path


def reconcile_one(bin_cmd: str, ip_dir: Path) -> dict | None:
    """Run the reconcile binary on one IP dir; return its parsed JSON or None."""
    cmd = shlex.split(bin_cmd) + ["reconcile", str(ip_dir), "--json"]
    try:
        out = subprocess.run(cmd, capture_output=True, text=True, timeout=120)
    except (OSError, subprocess.TimeoutExpired) as e:
        print(f"  {ip_dir.name}: reconcile failed ({e})", file=sys.stderr)
        return None
    if not out.stdout.strip():
        return None
    try:
        payload = json.loads(out.stdout)
    except json.JSONDecodeError:
        return None
    return payload.get("ips", [{}])[0] if payload.get("ips") else {}


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--ips-dir", required=True, help="dir of IP checkouts (each subdir an IP)")
    ap.add_argument("--bin", default="vyges metadata", help="reconcile binary invocation")
    ap.add_argument("--index", default="reconcile-index.json")
    ap.add_argument("--report", default="RECONCILE.md")
    ap.add_argument("--generated-at", default="", help="ISO-8601 timestamp (CI passes `date -u`)")
    args = ap.parse_args()

    ips_root = Path(args.ips_dir)
    ip_dirs = sorted(p for p in ips_root.iterdir() if p.is_dir() and (p / "vyges-metadata.json").exists())

    rows = []
    for d in ip_dirs:
        res = reconcile_one(args.bin, d)
        if res is None:
            continue
        findings = res.get("findings", [])
        gaps = sum(1 for f in findings if f.get("severity") == "GAP")
        drifts = sum(1 for f in findings if f.get("severity") == "DRIFT")
        rows.append({
            "ip": res.get("ip_name", d.name),
            "rtl_available": res.get("rtl_available", True),
            "gaps": gaps,
            "drifts": drifts,
        })

    total_gaps = sum(r["gaps"] for r in rows)
    total_drifts = sum(r["drifts"] for r in rows)
    drifting = sum(1 for r in rows if r["drifts"] > 0)
    clean = sum(1 for r in rows if r["gaps"] == 0 and r["drifts"] == 0)

    index = {
        "schema": "vyges-ip-catalog/reconcile-index-v1",
        "generated_at": args.generated_at,
        "total_ips": len(rows),
        "clean": clean,
        "drifting": drifting,
        "total_gaps": total_gaps,
        "total_drifts": total_drifts,
        "ips": sorted(rows, key=lambda r: (-r["drifts"], -r["gaps"], r["ip"])),
    }
    Path(args.index).write_text(json.dumps(index, indent=2) + "\n")

    lines = [
        "# Metadata ↔ RTL reconcile report",
        "",
        f"- **Generated:** {args.generated_at or 'n/a'}",
        f"- **IPs reconciled:** {len(rows)}",
        f"- **Clean (no gaps/drift):** {clean}",
        f"- **With drift (stale metadata):** {drifting}",
        f"- **Total gaps / drifts:** {total_gaps} / {total_drifts}",
        "",
        "> Report-only catalog health signal. Per-repo gating is each IP's own",
        "> `metadata-check` workflow. DRIFT = metadata claims something the RTL",
        "> lacks; GAP = RTL has something the metadata omits.",
        "",
        "| IP | drifts | gaps |",
        "| --- | ---: | ---: |",
    ]
    for r in index["ips"]:
        if r["drifts"] or r["gaps"]:
            lines.append(f"| {r['ip']} | {r['drifts']} | {r['gaps']} |")
    Path(args.report).write_text("\n".join(lines) + "\n")

    print(f"reconcile-index: {len(rows)} IP(s); {drifting} drifting, {total_gaps} gap(s), {total_drifts} drift(s)")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
