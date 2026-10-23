#!/usr/bin/env python3
"""make_captions.py — transcribe a clip and write timed captions (SRT/ASS).

PRODUCTION-PHASE tool. Transcription engine: faster-whisper, ALREADY
installed on this VM (research shortlist #5) — so unlike the other tools
this one is functional as soon as a clip exists; word-level karaoke timing
(WhisperX) is a later trial.

Usage:
  python3 tools/make_captions.py --clip build/2026-10-23/meme-01.mp4 \
      [--out build/2026-10-23/captions.srt] [--model base] [--language hi]
"""
from __future__ import annotations

import argparse
import os
import sys


def ts(seconds: float, ass: bool = False) -> str:
    h = int(seconds // 3600)
    m = int((seconds % 3600) // 60)
    s = seconds % 60
    if ass:
        return f"{h}:{m:02d}:{s:05.2f}"
    return f"{h:02d}:{m:02d}:{s:06.3f}".replace(".", ",")


def main() -> int:
    ap = argparse.ArgumentParser(description="Transcribe a clip to timed captions")
    ap.add_argument("--clip", required=True, help="input video/audio file")
    ap.add_argument("--out", default="", help="output .srt/.ass (default: alongside the clip)")
    ap.add_argument("--model", default="base", help="faster-whisper model size")
    ap.add_argument("--language", default="", help="language code (empty = auto-detect)")
    args = ap.parse_args()

    if not os.path.exists(args.clip):
        print(f"clip not found: {args.clip}", file=sys.stderr)
        return 1
    try:
        from faster_whisper import WhisperModel
    except ImportError:
        print("faster-whisper not importable in this environment", file=sys.stderr)
        return 2

    out = args.out or os.path.splitext(args.clip)[0] + ".srt"
    ass = out.endswith(".ass")
    model = WhisperModel(args.model, device="cpu", compute_type="int8")
    segments, _info = model.transcribe(args.clip, language=args.language or None)
    lines = []
    if ass:
        lines += ["[Script Info]", "ScriptType: v4.00+", "",
                  "[V4+ Styles]",
                  "Format: Name, Fontname, Fontsize, PrimaryColour, Bold, Alignment, MarginV",
                  "Style: Default,Arial,54,&H00FFFFFF,1,2,120", "",
                  "[Events]", "Format: Start, End, Style, Text"]
    for i, seg in enumerate(segments, 1):
        text = seg.text.strip()
        if ass:
            lines.append(f"Dialogue: 0,{ts(seg.start, True)},{ts(seg.end, True)},Default,,,{text}")
        else:
            lines += [str(i), f"{ts(seg.start)} --> {ts(seg.end)}", text, ""]
    with open(out, "w", encoding="utf-8") as f:
        f.write("\n".join(lines))
    print(f"captions -> {out} ({len(lines)} lines)")
    return 0


if __name__ == "__main__":
    sys.exit(main())
