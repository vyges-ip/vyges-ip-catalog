#!/usr/bin/env python3
"""Crawl every repo in a GitHub org and mirror each vyges-metadata.json.

Designed to run as a GitHub Action — uses GITHUB_TOKEN for auth (avoids
rate limits) and only writes files when content changes (avoids no-op
commits).

Output layout (Layer 1 source-of-truth — see README):
    metadata/<repo-name>.json   — verbatim vyges-metadata.json per IP
    index.json                  — slim change-detection index:
                                  [{repo, name, version, content_hash,
                                    default_branch, manifest_path}]
                                  Consumed by vycatalog-service's
                                  sync-from-registry-per-ip to skip
                                  unchanged IPs without per-file fetch.
    SUMMARY.md                  — human-readable counts + last-sync timestamp

The consolidated `catalog.json` that earlier versions emitted here is no
longer produced — aggregation is owned by vycatalog-service's
`GET /catalog.json` endpoint. See the 3-layer architecture diagram in
README.md.

Usage:
    python sync_metadata.py --org vyges-ip --output .
"""

from __future__ import annotations

import argparse
import datetime as dt
import hashlib
import json
import os
import sys
import urllib.error
import urllib.request
from pathlib import Path
from typing import Dict, List, Optional, Tuple


GITHUB_API = "https://api.github.com"
RAW_BASE   = "https://raw.githubusercontent.com"

# Repos in the org that are not IP packages and must never appear in the
# catalog. Add new entries here if more org-management repos land later.
EXCLUDED_REPOS = {
    "vyges-ip-catalog",  # this repo (don't index ourselves)
    "ip-template",       # IP scaffolding template, not a real IP
    ".github",           # org-level community files
}


def gh_request(url: str, token: Optional[str]) -> Tuple[int, bytes, dict]:
    req = urllib.request.Request(url, headers={
        "User-Agent":   "vyges-ip-catalog-sync",
        "Accept":       "application/vnd.github+json",
        "X-GitHub-Api-Version": "2022-11-28",
    })
    if token:
        req.add_header("Authorization", f"Bearer {token}")
    try:
        with urllib.request.urlopen(req, timeout=30) as resp:
            return resp.status, resp.read(), dict(resp.headers)
    except urllib.error.HTTPError as e:
        return e.code, e.read() if e.fp else b"", dict(e.headers or {})


def list_repos(org: str, token: Optional[str]) -> List[Dict]:
    repos: List[Dict] = []
    page = 1
    while True:
        url = f"{GITHUB_API}/orgs/{org}/repos?per_page=100&page={page}&type=public"
        status, body, _ = gh_request(url, token)
        if status != 200:
            print(f"ERROR listing repos page {page}: HTTP {status}", file=sys.stderr)
            sys.exit(1)
        page_data = json.loads(body)
        if not page_data:
            break
        repos.extend(page_data)
        page += 1
    return repos


def fetch_metadata(repo_name: str, default_branch: str,
                   token: Optional[str]) -> Optional[Dict]:
    """Fetch raw vyges-metadata.json for a single repo. Returns None if absent."""
    for branch in (default_branch, "main", "master"):
        if not branch:
            continue
        url = f"{RAW_BASE}/{repo_name}/{branch}/vyges-metadata.json"
        try:
            req = urllib.request.Request(url, headers={"User-Agent": "vyges-ip-catalog-sync"})
            if token:
                req.add_header("Authorization", f"Bearer {token}")
            with urllib.request.urlopen(req, timeout=20) as resp:
                if resp.status == 200:
                    return json.loads(resp.read())
        except urllib.error.HTTPError as e:
            if e.code == 404:
                continue
            print(f"  WARN {repo_name}: HTTP {e.code} on {branch}", file=sys.stderr)
        except Exception as e:
            print(f"  WARN {repo_name}: {e}", file=sys.stderr)
    return None


def write_if_changed(path: Path, content: str) -> bool:
    """Write content to path only if it differs. Returns True if written."""
    if path.exists() and path.read_text() == content:
        return False
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(content)
    return True


def manifest_hash(md: Dict) -> str:
    canonical = json.dumps(md, sort_keys=True, separators=(",", ":"))
    return hashlib.sha256(canonical.encode()).hexdigest()


def main() -> int:
    p = argparse.ArgumentParser()
    p.add_argument("--org", required=True, help="GitHub org to crawl (e.g. vyges-ip)")
    p.add_argument("--output", default=".",
                   help="Directory to write metadata/ + index.json")
    p.add_argument("--prune", action="store_true",
                   help="Remove metadata/<repo>.json for repos no longer present")
    args = p.parse_args()

    token = os.environ.get("GITHUB_TOKEN")
    if not token:
        print("WARN: GITHUB_TOKEN not set — may hit rate limits", file=sys.stderr)

    out = Path(args.output).resolve()
    metadata_dir = out / "metadata"
    metadata_dir.mkdir(parents=True, exist_ok=True)

    # Drop the old consolidated catalog.json — aggregation now lives in
    # vycatalog-service. Removing here prevents downstream tools from
    # silently binding to the stale file.
    legacy_catalog = out / "catalog.json"
    legacy_dropped = legacy_catalog.exists()
    if legacy_dropped:
        legacy_catalog.unlink()

    print(f"Listing repos in {args.org}...")
    repos = list_repos(args.org, token)
    print(f"  found {len(repos)} repos")

    index_entries: List[Dict] = []
    have_metadata: List[str] = []
    no_metadata:   List[str] = []
    written = 0

    for repo in sorted(repos, key=lambda r: r["name"]):
        full_name      = repo["full_name"]            # vyges-ip/<name>
        default_branch = repo.get("default_branch", "main")
        archived       = repo.get("archived", False)
        if archived:
            print(f"  skip (archived): {full_name}")
            continue
        if repo["name"] in EXCLUDED_REPOS:
            print(f"  skip (excluded): {full_name}")
            continue

        md = fetch_metadata(full_name, default_branch, token)
        if md is None:
            no_metadata.append(full_name)
            continue

        per_ip_path = metadata_dir / f"{repo['name']}.json"
        rendered = json.dumps(md, indent=2) + "\n"
        if write_if_changed(per_ip_path, rendered):
            written += 1

        # Slim index entry — enough for vycatalog-service to change-detect
        # without fetching the full manifest. NO full manifest here; that
        # lives in the per-IP file.
        index_entries.append({
            "repo":           full_name,
            "name":           md.get("name", repo["name"]),
            "version":        md.get("version") or md.get("x-version"),
            "content_hash":   manifest_hash(md),
            "default_branch": default_branch,
            "metadata_path":  f"metadata/{repo['name']}.json",
            "manifest_url":   f"{RAW_BASE}/{full_name}/{default_branch}/vyges-metadata.json",
        })
        have_metadata.append(full_name)

    # Prune stale per-IP files
    pruned = 0
    if args.prune:
        live_names = {r["name"] for r in repos}
        for f in metadata_dir.glob("*.json"):
            if f.stem not in live_names:
                f.unlink()
                pruned += 1

    now = dt.datetime.now(dt.timezone.utc).replace(microsecond=0).isoformat()

    # index.json — cheap change-detection manifest.
    #
    # `generated_sha` captures the commit SHA of the workflow run that
    # produced this index. Consumers use it as a Tier-1 early-exit
    # (stored value == current value → nothing changed, one HTTP request
    # total). Sourced from the GH Action's $GITHUB_SHA so the check
    # never has to hit api.github.com — important because GitHub's REST
    # API is IPv4-only and many IPv6-first hosts can't reach it.
    repo_slug  = os.environ.get("GITHUB_REPOSITORY", "")
    generated_sha = os.environ.get("GITHUB_SHA", "")
    index_doc = {
        "schema":        "vyges-ip-catalog/index-v1",
        "generated_at":  now,
        "generated_sha": generated_sha,
        "repo":          repo_slug,
        "org":           args.org,
        "repo_count":    len(repos),
        "with_metadata":    len(have_metadata),
        "without_metadata": len(no_metadata),
        "ips":           index_entries,
    }
    index_text = json.dumps(index_doc, indent=2) + "\n"
    index_changed = write_if_changed(out / "index.json", index_text)

    # Summary
    summary_lines = [
        f"# vyges-ip-catalog — sync summary",
        "",
        f"- **Generated:** {now}",
        f"- **Org:** `{args.org}`",
        f"- **Total repos:** {len(repos)}",
        f"- **With metadata:** {len(have_metadata)}",
        f"- **Without metadata:** {len(no_metadata)}",
        f"- **Per-IP files written this run:** {written}",
        f"- **Per-IP files pruned this run:** {pruned}",
        f"- **index.json changed:** {'yes' if index_changed else 'no'}",
        f"- **legacy catalog.json removed:** {'yes' if legacy_dropped else 'no'}",
        "",
    ]
    if no_metadata:
        summary_lines.append("## Repos without `vyges-metadata.json`")
        summary_lines.append("")
        summary_lines.extend(f"- {r}" for r in no_metadata)
        summary_lines.append("")
    write_if_changed(out / "SUMMARY.md", "\n".join(summary_lines))

    print(f"Done. {len(have_metadata)} have metadata, {len(no_metadata)} don't. "
          f"{written} per-IP files updated, index.json {'updated' if index_changed else 'unchanged'}.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
