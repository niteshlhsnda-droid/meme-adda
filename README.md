# Meme Adda 😂 — Trend Adda

**Dashboard:** https://niteshlhsnda-droid.github.io/meme-adda/
**Channels:** YouTube [@memeaddaindia](https://www.youtube.com/@memeaddaindia) · Instagram [@memeaddaindia.post](https://www.instagram.com/memeaddaindia.post/)

Roz ke memes, desi style. Original Hinglish memes + Shorts — scratch se bante hain, repost kabhi nahi.

📖 **How we make memes — [MEME-PLAYBOOK.md](MEME-PLAYBOOK.md)**: trend × movie/TV scene = meme. The full method, scene bank and QC rules.

This repo is Meme Adda's foundation, built the **Patna Pulse way** (founder order, 2026-10-23):

**research → GitHub → install → production** — in that order, no phase skipped.

| Phase | Status |
|---|---|
| 1. Research | ✅ Done — `research/2026-10-23-reset-research.md` |
| 2. GitHub (this repo + dashboard) | ✅ Done |
| 3. Install (yt-dlp → MoviePy → local memegen → PRAW) | ⏳ Next |
| 4. Production (daily memes, posted + read-back verified) | 🔒 Starts only after 3 |

## How it works (mirrors patna-pulse 1:1)

- `watch.py` — trend collector (stdlib-only): Reddit meme subs (origin layer) +
  Google Trends IN RSS (confirmation) + `curated.json` (hand-picked + founder's
  scene tips) → **`trends.json`**. Heat = independent-source count:
  3+ = 🔥 verified trend, 2 = rising, 1 = watch.
- `index.html` / `styles.css` / `app.js` — the dashboard (above): today's
  trends with heat, the template library, the production queue.
- `templates/templates.json` — Desi reaction-template DB (Hera Pheri,
  Jethalal, Shark Tank India…), every entry with a **rights note**.
  `templates/frames/` holds template stills/clips in the production phase.
- `tools/` — the pipeline: `fetch_clip.py` (yt-dlp wrapper + provenance log),
  `build_meme.py` (two-clip assembler), `make_captions.py` (faster-whisper →
  timed captions), `publish_trends.py` / `publish_site.py` (GitHub-API PUTs,
  no Actions), `post_and_verify.py` (post → **read-back verify** → only then
  mark posted).
- `state/` — `posted.json` (dedupe), `used_templates.json` (rotation),
  `queue.json` (trend → scripted → built → posted).
- `build/YYYY-MM-DD/` — per-day production dirs (never /tmp).
- `research/` — the reset research report + ecosystem notes.
- `channel-setup.md` — the brand pack (single source of truth).

## Daily workflow (production phase)

Morning + late-afternoon `watch.py` → dashboard shows verified/rising trends
→ pick 2 (1 evergreen template + 1 trend-jack) → scenes via `curated.json` /
`fetch_clip.py` with provenance logged → `build_meme.py` assembles → frames
eyeballed (visual QC) → post IG Reel + YT Short in the 7–9 PM IST window via
`post_and_verify.py` → `state/` updated **only after read-back**.

## Format + risk rules (from the research, §2f)

Founder's format: two-video **"connect the dots"** memes — own setup clip +
TV/movie reaction clip as punchline. Production discipline that keeps the
format on the right side of platform rules: borrowed clips stay short and
subordinate to our own edit; narrative captions carry the joke (reaction
*with* commentary, not clips stitched with no story); template/original
content is the majority of volume; Content ID claims are a cost of business
(revenue to claimant, not a strike) — formal strikes and reused-content
flags are the real risks and both are managed by the discipline above.
