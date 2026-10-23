#!/usr/bin/env python3
"""publish_trends.py — PUT trends.json to the meme-adda repo via the GitHub
API (the publish_data_json.py role from Patna Pulse). Thin wrapper over
publish_site.py restricted to the trend data, for the 2x/day watch runs.

Usage: python3 tools/publish_trends.py [--dry-run]
"""
from __future__ import annotations

import subprocess
import sys
import os

HERE = os.path.dirname(os.path.abspath(__file__))


def main() -> int:
    cmd = [sys.executable, os.path.join(HERE, "publish_site.py"), "--only", "trends.json"]
    if "--dry-run" in sys.argv:
        cmd.append("--dry-run")
    return subprocess.call(cmd)


if __name__ == "__main__":
    sys.exit(main())
