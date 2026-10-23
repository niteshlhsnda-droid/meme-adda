#!/usr/bin/env python3
"""build_meme.py — two-clip assembler (the assemble_news_reel.py role).

PRODUCTION-PHASE tool: assembles the founder's "connect the dots" format —
own setup clip + TV/movie reaction clip as punchline — into a 1080x1920
vertical video with the hook text burned in and timed captions.

INSTALL-PHASE dependency: MoviePy (shortlist #2) with ffmpeg underneath.
Until MoviePy lands, this skeleton validates its inputs and prints the
ffmpeg plan it will execute; it never fabricates an output video.

Usage:
  python3 tools/build_meme.py --setup setup.mp4 --reaction reaction.mp4 \
      --hook "POV: salary day" --captions captions.ass \
      --out build/2026-10-23/meme-01.mp4 [--dry-run]
"""
from __future__ import annotations

import argparse
import os
import shutil
import sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
W, H = 1080, 1920


def check(path: str, label: str) -> bool:
    if not path:
        return True
    if not os.path.exists(path):
        print(f"{label} not found: {path}", file=sys.stderr)
        return False
    return True


def main() -> int:
    ap = argparse.ArgumentParser(description="Assemble a two-clip meme (MoviePy/ffmpeg, production phase)")
    ap.add_argument("--setup", required=True, help="setup clip (our own / sourced, provenance logged)")
    ap.add_argument("--reaction", required=True, help="reaction clip (template library / fetched scene)")
    ap.add_argument("--hook", required=True, help="<=5-word hook text for the first frame")
    ap.add_argument("--captions", default="", help="timed captions file (.ass/.srt) from make_captions.py")
    ap.add_argument("--out", required=True, help="output mp4 path, under build/YYYY-MM-DD/")
    ap.add_argument("--dry-run", action="store_true", help="validate inputs and print the plan only")
    args = ap.parse_args()

    ok = check(args.setup, "setup") and check(args.reaction, "reaction") \
        and check(args.captions, "captions")
    if not ok:
        return 1

    plan = [
        f"scale/pad both clips to {W}x{H} (9:16), setup first, reaction as punchline",
        f"burn hook text on first frame: {args.hook!r}",
        "burn timed captions" if args.captions else "no captions file (skip burn-in)",
        "loudnorm audio, hook frame held ~0.4s, export H.264 + AAC",
        f"output -> {args.out}",
    ]
    print("build plan:")
    for step in plan:
        print(f"  - {step}")

    if args.dry_run:
        print("dry-run: nothing assembled")
        return 0
    try:
        import moviepy  # noqa: F401  (install phase)
    except ImportError:
        print("MoviePy is not installed yet — that is the INSTALL phase. "
              "Plan printed; nothing assembled.", file=sys.stderr)
        return 2
    if shutil.which("ffmpeg") is None:
        print("ffmpeg missing", file=sys.stderr)
        return 2
    # Production-phase implementation point: MoviePy concatenate_videoclips
    # + TextClip hook + CompositeVideoClip captions, per the plan above.
    print("MoviePy present — assembly implementation lands in the production phase.",
          file=sys.stderr)
    return 2


if __name__ == "__main__":
    sys.exit(main())
