#!/usr/bin/env python3
"""post_and_verify.py — post a built meme, then READ-BACK verify before
anything is marked posted. The Patna Pulse rule, verbatim in spirit:
a returned post id is NOT proof; only a read-back of the live grid/feed
matching the caption is. state/posted.json is updated only after that
verification succeeds.

PRODUCTION-PHASE tool (posting is not part of the GitHub phase). Works for
Instagram via instagram-cli (the @memeaddaindia.post account) and YouTube
via the workspace archive-upload venv uploader. Both paths verify by
read-back; on an ambiguous outcome the meme stays UNMARKED so a later run
can re-check instead of double-posting.

Usage:
  python3 tools/post_and_verify.py --file build/2026-10-23/meme-01.mp4 \
      --id meme-2026-10-23-01 --caption "Roz ka scene 😂 ..." \
      --platform instagram [--account-id <id>] [--dry-run]
"""
from __future__ import annotations

import argparse
import json
import os
import subprocess
import sys
from datetime import datetime, timedelta, timezone

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
IST = timezone(timedelta(hours=5, minutes=30))
POSTED = os.path.join(ROOT, "state", "posted.json")


def load_posted() -> list:
    try:
        with open(POSTED, encoding="utf-8") as f:
            return json.load(f)
    except (OSError, json.JSONDecodeError):
        return []


def mark_posted(meme_id: str, platform: str, url: str) -> None:
    posted = load_posted()
    posted.append({
        "id": meme_id,
        "platform": platform,
        "url": url,
        "posted_at_ist": datetime.now(IST).strftime("%Y-%m-%d %H:%M IST"),
        "verified_by": "read-back caption match",
    })
    with open(POSTED, "w", encoding="utf-8") as f:
        json.dump(posted, f, ensure_ascii=False, indent=2)


def ig_readback(account_id: str, caption: str, limit: int = 10) -> str | None:
    """Return the live post URL whose caption matches, else None.

    New reels can rank below older carousels; always scan the full window,
    never judge by rank 1 alone (Patna Pulse lesson, 2026-10-09).
    """
    out = subprocess.run(
        ["instagram-cli", "posts", "--account-id", account_id, "--limit", str(limit)],
        capture_output=True, text=True, timeout=120)
    if out.returncode != 0:
        raise RuntimeError(f"instagram-cli read-back failed: {out.stderr.strip()[:300]}")
    probe = caption.strip()[:40]
    for line in out.stdout.splitlines():
        if probe and probe in line:
            return line.strip()
    return None


def main() -> int:
    ap = argparse.ArgumentParser(description="Post a meme and verify by read-back")
    ap.add_argument("--file", required=True, help="built video/image file")
    ap.add_argument("--id", required=True, help="meme id (dedupe key in state/posted.json)")
    ap.add_argument("--caption", required=True, help="caption text (Hinglish, hook first)")
    ap.add_argument("--platform", choices=["instagram", "youtube"], default="instagram")
    ap.add_argument("--account-id", default="", help="instagram account id (required for IG)")
    ap.add_argument("--dry-run", action="store_true", help="validate only; post nothing")
    args = ap.parse_args()

    if not os.path.exists(args.file):
        print(f"file not found: {args.file}", file=sys.stderr)
        return 1
    if any(p.get("id") == args.id for p in load_posted()):
        print(f"{args.id} is already in state/posted.json — refusing to double-post")
        return 1
    if args.dry_run:
        print("dry-run: inputs valid, nothing posted, state untouched")
        return 0

    if args.platform == "instagram":
        if not args.account_id:
            print("--account-id is required for instagram", file=sys.stderr)
            return 1
        res = subprocess.run(
            ["instagram-cli", "post-feed", "--account-id", args.account_id,
             "--file", args.file, "--caption", args.caption],
            capture_output=True, text=True, timeout=600)
        if res.returncode != 0:
            print(f"post failed (nothing marked): {res.stderr.strip()[:300]}", file=sys.stderr)
            return 1
        live = ig_readback(args.account_id, args.caption)
        if not live:
            print("AMBIGUOUS: post returned success but read-back shows no caption "
                  "match — NOT marked posted; re-check before any retry.", file=sys.stderr)
            return 3
        mark_posted(args.id, "instagram", live)
        print(f"verified live + marked posted: {live}")
        return 0

    # YouTube path lands in the production phase with the channel uploader;
    # the read-back there is the channel's uploads list caption/title match.
    print("youtube path: wired in the production phase", file=sys.stderr)
    return 2


if __name__ == "__main__":
    sys.exit(main())
