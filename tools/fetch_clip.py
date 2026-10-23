#!/usr/bin/env python3
"""fetch_clip.py — fetch a scene clip into a build dir, with provenance logged.

INSTALL-PHASE tool: the real fetch runs through yt-dlp (shortlist #1 in
research/2026-10-23-reset-research.md), which is NOT installed yet. Until
then this skeleton validates arguments, prepares the build dir and appends
the provenance record the production phase will rely on — every clip file
in templates/frames/ and build/ must have a source-log entry.

Usage:
  python3 tools/fetch_clip.py --url <video-url> --start 00:12 --end 00:19 \
      --slug punisher-wait [--date YYYY-MM-DD] [--dry-run]
"""
from __future__ import annotations

import argparse
import json
import os
import shutil
import subprocess
import sys
from datetime import date

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


def main() -> int:
    ap = argparse.ArgumentParser(description="Fetch a scene clip (yt-dlp wrapper, install phase)")
    ap.add_argument("--url", required=True, help="source video URL (YouTube/IG/X)")
    ap.add_argument("--start", required=True, help="clip start, HH:MM:SS or MM:SS")
    ap.add_argument("--end", required=True, help="clip end, HH:MM:SS or MM:SS")
    ap.add_argument("--slug", required=True, help="short kebab-case name for the clip")
    ap.add_argument("--date", default=date.today().isoformat(), help="build date (default: today)")
    ap.add_argument("--dry-run", action="store_true", help="log provenance only, fetch nothing")
    args = ap.parse_args()

    build_dir = os.path.join(ROOT, "build", args.date)
    os.makedirs(build_dir, exist_ok=True)
    out_path = os.path.join(build_dir, f"{args.slug}.mp4")

    record = {
        "slug": args.slug,
        "url": args.url,
        "start": args.start,
        "end": args.end,
        "file": os.path.relpath(out_path, ROOT),
        "fetched": False,
    }
    log_path = os.path.join(build_dir, "sources.json")
    log = []
    if os.path.exists(log_path):
        with open(log_path, encoding="utf-8") as f:
            log = json.load(f)
    log.append(record)
    with open(log_path, "w", encoding="utf-8") as f:
        json.dump(log, f, ensure_ascii=False, indent=2)
    print(f"provenance logged -> {log_path} ({args.slug})")

    if args.dry_run:
        print("dry-run: nothing fetched")
        return 0
    if shutil.which("yt-dlp") is None:
        print("yt-dlp is not installed yet — that is the INSTALL phase. "
              "Provenance is logged; fetch nothing.", file=sys.stderr)
        return 2
    # Install-phase implementation point: yt-dlp --download-sections.
    cmd = ["yt-dlp", "-f", "mp4", "--download-sections",
           f"*{args.start}-{args.end}", "-o", out_path, args.url]
    print("running:", " ".join(cmd))
    return subprocess.call(cmd)


if __name__ == "__main__":
    sys.exit(main())
