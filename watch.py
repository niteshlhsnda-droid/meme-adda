#!/usr/bin/env python3
"""Meme Adda trend collector — the meme equivalent of Patna Pulse's generate.py.

Stdlib-only (runs before the install phase; no PRAW / yt-dlp needed yet).
Pulls, 2x/day ahead of the 7-9 PM IST posting window:
  * Reddit public JSON listings (hot + rising) for the configured meme subs
    (the origin layer — most image memes are first published on Reddit),
  * Google Trends India "Trending now" RSS (confirmation layer),
  * curated.json (hand-picked items + the founder's scene tips),
then writes trends.json. Heat = number of INDEPENDENT sources carrying an
item (same rule as Patna Pulse's genuineness score):
  3+ sources = verified trend, 2 = rising, 1 = single/watch.

Usage: python3 watch.py [--out trends.json] [--limit 25]
Exit code is 0 even when a source is unreachable (the run is recorded in
trends.json -> source_status); it is non-zero only if NOTHING could be
collected AND no curated items exist, in which case trends.json is seeded
from templates/templates.json so the dashboard never renders empty.
"""
from __future__ import annotations

import argparse
import json
import os
import re
import sys
import urllib.request
import xml.etree.ElementTree as ET
from datetime import datetime, timedelta, timezone

HERE = os.path.dirname(os.path.abspath(__file__))
IST = timezone(timedelta(hours=5, minutes=30))
UA = "meme-adda-watch/0.1 (trend research; contact via github repo)"

REDDIT_SUBS = ["IndianDankMemes", "dankmemes", "memes"]
GTRENDS_RSS = "https://trends.google.com/trending/rss?geo=IN"


def fetch(url: str, timeout: int = 20) -> bytes:
    req = urllib.request.Request(url, headers={"User-Agent": UA})
    with urllib.request.urlopen(req, timeout=timeout) as resp:
        return resp.read()


def slugify(text: str) -> str:
    slug = re.sub(r"[^a-z0-9]+", "-", text.lower()).strip("-")
    return slug[:60] or "item"


def norm_title(text: str) -> str:
    return re.sub(r"\s+", " ", re.sub(r"[^a-z0-9 ]", "", text.lower())).strip()


def reddit_items(limit: int) -> list[dict]:
    items = []
    for sub in REDDIT_SUBS:
        for listing in ("hot", "rising"):
            url = f"https://www.reddit.com/r/{sub}/{listing}.json?limit={limit}"
            try:
                data = json.loads(fetch(url))
            except Exception as e:  # recorded by caller via source_status
                raise RuntimeError(f"r/{sub}/{listing}: {e}") from e
            for child in data.get("data", {}).get("children", []):
                d = child.get("data", {})
                if d.get("stickied"):
                    continue
                items.append({
                    "title": d.get("title", "").strip(),
                    "url": "https://www.reddit.com" + d.get("permalink", ""),
                    "source": f"reddit:r/{sub}",
                    "kind": "reddit-post",
                    "score": d.get("score", 0),
                })
    return items


def gtrends_items() -> list[dict]:
    raw = fetch(GTRENDS_RSS)
    root = ET.fromstring(raw)
    items = []
    for item in root.iter("item"):
        title = (item.findtext("title") or "").strip()
        link = (item.findtext("link") or "").strip()
        if title:
            items.append({
                "title": title,
                "url": link or GTRENDS_RSS,
                "source": "google-trends-in",
                "kind": "search-trend",
                "score": 0,
            })
    return items


def curated_items(path: str) -> list[dict]:
    try:
        with open(path, encoding="utf-8") as f:
            data = json.load(f)
    except (OSError, json.JSONDecodeError):
        return []
    items = []
    for entry in data if isinstance(data, list) else []:
        title = (entry.get("title") or "").strip()
        if not title:
            continue
        items.append({
            "title": title,
            "url": entry.get("url", ""),
            "source": "curated",
            "kind": entry.get("kind", "curated"),
            "score": 0,
            "note": entry.get("note", ""),
        })
    return items


def seed_items() -> list[dict]:
    """Fallback: the report's verified evergreen templates, marked seeded."""
    path = os.path.join(HERE, "templates", "templates.json")
    try:
        with open(path, encoding="utf-8") as f:
            templates = json.load(f)
    except (OSError, json.JSONDecodeError):
        return []
    return [{
        "title": t.get("name", ""),
        "url": t.get("source_url", ""),
        "source": "seeded:reset-research-2026-10-23",
        "kind": "template",
        "score": 0,
        "seeded": True,
    } for t in templates if t.get("name")]


def cluster(items: list[dict]) -> list[dict]:
    """Group near-identical titles; heat = independent-source count."""
    groups: dict[str, dict] = {}
    for it in items:
        key = norm_title(it["title"])
        if not key:
            continue
        g = groups.setdefault(key, {
            "id": slugify(it["title"]),
            "title": it["title"],
            "url": it["url"],
            "sources": set(),
            "kind": it["kind"],
            "score": 0,
            "seeded": bool(it.get("seeded")),
            "note": it.get("note", ""),
        })
        g["sources"].add(it["source"])
        g["score"] = max(g["score"], it.get("score", 0))
        if it.get("seeded"):
            g["seeded"] = True
    trends = []
    for g in groups.values():
        n = len(g["sources"])
        g["source_count"] = n
        g["heat"] = n
        g["label"] = "verified" if n >= 3 else "rising" if n == 2 else "watch"
        g["sources"] = sorted(g["sources"])
        trends.append(g)
    trends.sort(key=lambda t: (t["source_count"], t["score"]), reverse=True)
    return trends


def main() -> int:
    ap = argparse.ArgumentParser(description="Collect meme trends into trends.json")
    ap.add_argument("--out", default=os.path.join(HERE, "trends.json"))
    ap.add_argument("--limit", type=int, default=25)
    args = ap.parse_args()

    status: dict[str, str] = {}
    items: list[dict] = []

    try:
        items += reddit_items(args.limit)
        status["reddit"] = "ok"
    except Exception as e:
        status["reddit"] = f"failed: {e}"

    try:
        items += gtrends_items()
        status["google_trends_in"] = "ok"
    except Exception as e:
        status["google_trends_in"] = f"failed: {e}"

    curated = curated_items(os.path.join(HERE, "curated.json"))
    items += curated
    status["curated"] = f"ok ({len(curated)} items)"

    seeded = False
    if status["reddit"].startswith("failed"):
        # Reddit is unreachable from this host (403 on every public endpoint):
        # top up with the report's verified evergreen templates, each marked
        # seeded with its source URL, so the origin layer is never empty.
        items += seed_items()
        seeded = True
        status["seed"] = "reddit unreachable; templates.json entries added as seeded"
    if not items:
        items = seed_items()
        seeded = True
        status["seed"] = "trends.json seeded from templates.json (all live sources unreachable)"

    trends = cluster(items)
    payload = {
        "generated_at_ist": datetime.now(IST).strftime("%d %b %Y, %I:%M %p IST"),
        "generated_by": "watch.py",
        "seeded": seeded,
        "source_status": status,
        "trend_count": len(trends),
        "trends": trends,
    }
    with open(args.out, "w", encoding="utf-8") as f:
        json.dump(payload, f, ensure_ascii=False, indent=2)

    print(f"watch.py: {len(trends)} trends -> {args.out}")
    for name, s in status.items():
        print(f"  source {name}: {s}")
    for t in trends[:5]:
        print(f"  [{t['label']}] ({t['source_count']} src) {t['title'][:80]}")
    return 0 if trends else 1


if __name__ == "__main__":
    sys.exit(main())
