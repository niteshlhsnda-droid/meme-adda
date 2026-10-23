#!/usr/bin/env python3
"""Publish the local meme-adda workspace to the GitHub repo via API PUTs.

Mirrors patna-pulse's tools/publish_data_json.py: for each file, GET the
repo copy; PUT only when bytes differ (with the remote sha), create when
missing. No GitHub Actions involved anywhere — Pages serves from the main
branch root. Idempotent: re-runs with no changes print UNCHANGED lines.

Usage: python3 tools/publish_site.py [--dry-run] [--only <repo-path>]
"""
from __future__ import annotations

import base64
import json
import os
import subprocess
import sys
import tempfile

_CANDIDATES = [
    "/home/hatch/workspace/custom-connectors/custom.legacy-github/bin/gh.py",
    "/home/hatch/workspace/skills/github/bin/gh.py",
]
GH = next((p for p in _CANDIDATES if os.path.exists(p)), _CANDIDATES[0])
OWNER = "niteshlhsnda-droid"
REPO = "meme-adda"
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
ARGV_BODY_LIMIT = 100_000

FILES = [
    "index.html", "styles.css", "app.js", "assets/mascot.jpg",
    "trends.json", "curated.json", "watch.py",
    "README.md", "channel-setup.md",
    "research/2026-10-23-reset-research.md", "research/channel-setup.md",
    "templates/templates.json", "templates/frames/.gitkeep", "templates/memegen/.gitkeep",
    "tools/fetch_clip.py", "tools/build_meme.py", "tools/make_captions.py",
    "tools/publish_trends.py", "tools/post_and_verify.py", "tools/publish_site.py",
    "state/posted.json", "state/used_templates.json", "state/queue.json",
    "build/.gitkeep",
]


def gh(method: str, path: str, data: dict | None = None) -> dict:
    cmd = [GH, method, path]
    tmp = None
    if data is not None:
        payload = json.dumps(data)
        if len(payload.encode("utf-8")) > ARGV_BODY_LIMIT:
            fd, tmp = tempfile.mkstemp(prefix="gh-body-", suffix=".json")
            with os.fdopen(fd, "w", encoding="utf-8") as f:
                f.write(payload)
            cmd += ["--data-file", tmp]
        else:
            cmd += ["--data", payload]
    try:
        out = subprocess.run(cmd, capture_output=True, text=True, timeout=120)
    finally:
        if tmp:
            try:
                os.remove(tmp)
            except OSError:
                pass
    if out.returncode != 0:
        raise RuntimeError(f"gh.py {method} {path} failed: {(out.stderr or out.stdout).strip()[:400]}")
    return json.loads(out.stdout) if out.stdout.strip() else {}


def remote_file(path: str) -> tuple[bytes | None, str | None]:
    try:
        res = gh("get", f"/repos/{OWNER}/{REPO}/contents/{path}")
    except RuntimeError:
        return None, None
    if isinstance(res, dict) and res.get("http_status", 200) >= 400:
        return None, None
    try:
        return base64.b64decode(res["content"]), res["sha"]
    except (KeyError, TypeError):
        return None, None


def publish_one(rel: str, dry: bool) -> str:
    local_path = os.path.join(ROOT, rel)
    with open(local_path, "rb") as f:
        local_bytes = f.read()
    remote_bytes, sha = remote_file(rel)
    if remote_bytes == local_bytes:
        return f"UNCHANGED {rel}"
    if dry:
        return f"DRY-RUN would PUT {rel} ({len(local_bytes)} bytes)"
    body = {
        "message": f"Publish {rel}",
        "content": base64.b64encode(local_bytes).decode("ascii"),
    }
    if sha:
        body["sha"] = sha
    res = gh("put", f"/repos/{OWNER}/{REPO}/contents/{rel}", body)
    return f"PUT {rel} -> {res['content']['path']} ({len(local_bytes)} bytes)"


def main() -> int:
    dry = "--dry-run" in sys.argv
    only = None
    if "--only" in sys.argv:
        only = sys.argv[sys.argv.index("--only") + 1]
    files = [only] if only else FILES
    for rel in files:
        print(publish_one(rel, dry))
    return 0


if __name__ == "__main__":
    sys.exit(main())
