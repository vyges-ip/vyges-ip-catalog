#!/usr/bin/env python3
"""Score every metadata/<repo>.json against the Vyges integration-readiness
rubric and emit:

    scores.json   — per-IP score + tier + breakdown + gaps (machine-readable)
    SCORES.md     — human-readable leaderboard + bottom-N + per-tier counts

Uses the canonical scorer from vyges/metadata-scorer-action. The action
exposes ``scorer.py`` via raw GitHub URL; we fetch it at runtime so this
repo never has its own copy of the rubric to drift.

Usage:
    python scripts/score_all.py --metadata-dir metadata --output .
                                [--scorer-ref v1] [--scorer-cache /tmp/...]
"""

from __future__ import annotations

import argparse
import importlib.util
import json
import sys
import urllib.request
from pathlib import Path


SCORER_URL_TPL = (
    "https://raw.githubusercontent.com/vyges/metadata-scorer-action/{ref}/scorer.py"
)


def _load_scorer(ref: str, cache_path: Path):
    """Fetch scorer.py from the action repo at the given ref + import it."""
    cache_path.parent.mkdir(parents=True, exist_ok=True)
    if not cache_path.exists():
        url = SCORER_URL_TPL.format(ref=ref)
        print(f"  fetching scorer from {url}")
        with urllib.request.urlopen(url, timeout=20) as resp:
            cache_path.write_bytes(resp.read())
    spec = importlib.util.spec_from_file_location("vyges_scorer", cache_path)
    mod = importlib.util.module_from_spec(spec)
    # Register before exec so dataclass field-type resolution can find the
    # module via sys.modules (otherwise IpScore's dataclass init crashes
    # under from __future__ import annotations).
    sys.modules["vyges_scorer"] = mod
    spec.loader.exec_module(mod)
    return mod


def _tier(score: int) -> str:
    if score >= 80:
        return "Good"
    if score >= 60:
        return "Medium"
    return "High-risk"


def main() -> int:
    p = argparse.ArgumentParser()
    p.add_argument("--metadata-dir", default="metadata")
    p.add_argument("--output", default=".")
    p.add_argument("--scorer-ref", default="v1",
                   help="metadata-scorer-action git ref (tag/branch/sha)")
    p.add_argument("--scorer-cache", default=".scorer-cache/scorer.py")
    args = p.parse_args()

    metadata_dir = Path(args.metadata_dir)
    out          = Path(args.output)
    if not metadata_dir.exists():
        print(f"ERROR: {metadata_dir} not found", file=sys.stderr)
        return 1

    scorer = _load_scorer(args.scorer_ref, Path(args.scorer_cache))

    results = []
    for f in sorted(metadata_dir.glob("*.json")):
        try:
            md = json.loads(f.read_text())
        except json.JSONDecodeError as e:
            print(f"  WARN {f.name}: {e}")
            continue
        score, breakdown, gaps = scorer.score_metadata(md)
        results.append({
            "ip":         f.stem,
            "score":      score,
            "tier":       _tier(score),
            "breakdown":  breakdown,
            "gaps":       gaps,
        })

    # Distribution
    tiers = {"Good": 0, "Medium": 0, "High-risk": 0}
    for r in results:
        tiers[r["tier"]] += 1
    aggregate = sum(r["score"] for r in results) // len(results) if results else 0

    # scores.json
    scores_doc = {
        "scorer_ref": args.scorer_ref,
        "ip_count":   len(results),
        "aggregate":  aggregate,
        "tiers":      tiers,
        "ips":        sorted(results, key=lambda r: (-r["score"], r["ip"])),
    }
    (out / "scores.json").write_text(json.dumps(scores_doc, indent=2) + "\n")

    # SCORES.md — leaderboard + bottom-N
    lines = [
        "# Vyges IP Catalog — Metadata Quality Scores",
        "",
        f"- **Aggregate:** {aggregate}/100",
        f"- **IPs scored:** {len(results)}",
        f"- **Good (≥80):** {tiers['Good']}",
        f"- **Medium (60–79):** {tiers['Medium']}",
        f"- **High-risk (<60):** {tiers['High-risk']}",
        f"- **Scorer:** [vyges/metadata-scorer-action@{args.scorer_ref}]"
        f"(https://github.com/vyges/metadata-scorer-action/tree/{args.scorer_ref})",
        "",
        "## Needs work (bottom 20)",
        "",
        "| IP | Score | Tier | Top gap |",
        "|---|---:|---|---|",
    ]
    bottom = sorted(results, key=lambda r: (r["score"], r["ip"]))[:20]
    for r in bottom:
        first_gap = (r["gaps"][0] if r["gaps"] else "—").replace("|", "\\|")
        lines.append(f"| `{r['ip']}` | {r['score']} | {r['tier']} | {first_gap} |")
    lines.extend([
        "",
        "## Top 20 (highest scores)",
        "",
        "| IP | Score |",
        "|---|---:|",
    ])
    for r in sorted(results, key=lambda r: (-r["score"], r["ip"]))[:20]:
        lines.append(f"| `{r['ip']}` | {r['score']} |")
    lines.append("")
    (out / "SCORES.md").write_text("\n".join(lines))

    print(f"Scored {len(results)} IPs. Aggregate {aggregate}/100. "
          f"Good={tiers['Good']} Medium={tiers['Medium']} "
          f"High-risk={tiers['High-risk']}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
