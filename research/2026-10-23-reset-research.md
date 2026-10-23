# Meme Adda — Reset Research Report

**Date:** 2026-10-23 · **Phase:** 1 of 4 (RESEARCH) · **Status: production PAUSED by founder order (2026-10-23)**

Founder's ruling: Meme Adda was started the wrong way round. The correct order is the Patna Pulse order —
**research → GitHub → install → production** — and nothing in the later phases starts until the earlier one is done.
This report is the research phase. No repos were created, nothing was installed, nothing was built or posted for this reset.

**What already exists (from the first, wrong-way start):** YouTube channel "Meme Adda" @memeaddaindia
(UCnQJQkNKfUv8GnE-Llkv-Jg, created 2026-10-21, no uploads), Instagram @memeaddaindia.post (created 2026-10-22,
profile picture set, one 5-meme launch carousel live). Founder's format decision of 2026-10-22 stands: two-video
"connect the dots" memes — a setup clip + a TV/movie reaction clip as the punchline. He said he has relevant scenes.
Brand pack: `~/workspace/meme-pilot/channel-setup.md`.

**The model being copied — Patna Pulse** (`~/workspace/patna-news-watch/` + repo `niteshlhsnda-droid/patna-pulse`):
`generate.py` collects Google News RSS (EN + HI) + hand-verified `curated.json`, clusters near-duplicates, scores
genuineness by independent-outlet count (3+ = verified, 2 = corroborated, 1 = single), writes `data.json`;
`tools/publish_data_json.py` PUTs `data.json` + images to the repo via the GitHub API; a static `index.html`/`app.js`
renders `data.json` on GitHub Pages; the hourly poster builds from `data.json`, dedupes against
`posted_story_ids.json` + `recent_reels.json`, posts once, and marks ids seen **only after a read-back verifies the
post is live**. Every Meme Adda design choice below maps to one of these parts.

---

## 1. Ecosystem — the Indian/Hinglish meme scene, 2025–26

### Instagram: the mega pages are media companies, not posters
Per Socialveins' Indian meme-page listing (crawled Oct 2026): **Sarcasm ~13.4M followers, RVCJ Media ~12.98M,
Trolls Official ~10.58M, ghantaa ~8.53M, Log Kya Sochenge ~7.15M** — all Mumbai-based.
Source: https://socialveins.com/influencers/lists/best-meme-pages-instagram-india
RVCJ (the original "Rajnikant vs CID Jokes") is now a 51–200-employee digital media and meme-marketing company,
founded 2010. Source: https://in.linkedin.com/company/rvcj-digital-media-pvt.-ltd.?trk=similar-pages

### What separates the growing pages from the dead ones (2026 ranking evidence)
Hobo's 2026 Indian meme-page index ranks by "cultural sentiment and share-velocity, not raw follower counts":
**#1 RVCJ Media — "fastest transition from news to meme"**; #2 TVF — highest shareability among corporate Gen Z;
#3 Sarcasm_Only — "masters of the relatability loop"; #4 Desi Humor — highest engagement in Tier-2/3 cities;
then The Indian Idiot (campus life), Dank Indian Memes (absurdist "chaos culture"), Bakchod Billi (desi nostalgia).
Source: https://hobo.video/blog/best-10-meme-pages-on-instagram-in-india-2026/amp/
The four winning traits, in order: **(1) speed on topical events, (2) shareability (DM-forward value),
(3) relatability loops, (4) regional/Tier-2-3 specificity.** A Patna-flavoured Hinglish page has trait (4) built in;
traits (1) and (2) are pipeline problems — exactly what the Patna-Pulse-style research pipeline solves.

### YouTube Shorts: clip-format channels reach billions of views
From youtubers.me's India People & Blogs top-500 crawl: **VootaTv- Memes — ~790K subscribers, ~1.92B views across
~220 videos; Filmista — ~563K subscribers, ~1.90B views across ~885 videos** — both built on movie/TV clip formats.
Source: https://us.youtubers.me/india/people-blogs/top-500-youtube-channels-in-india
(Views at that scale are real; whether those views are *monetised* is a separate question — see §2.)
YouTube India's official 2025 lists show the meme fuel supply is cinema + cricket + internet phenomena mixed:
trending topics included Coolie, IPL 2025, Saiyaara, Kumbh Mela, Asia Cup, Labubu, TungTungTung Sahur — and
**76% of Indian Gen Z say they come to YouTube to understand global events and trends**, i.e. the audience treats
Shorts as its trend feed. Source: https://mediabrief.com/youtube-indias-end-of-year-lists/

### Cadence and timing that work in India
- Instagram performs best **12–2 PM and 7–10 PM IST**; YouTube peaks **6–9 PM IST** (evenings, post school/work).
  Source: https://hobo.video/blog/peak-engagement-times-for-influencer-content-on-instagram-youtube/
- Independent 2026 guide agrees: IG weekdays 6–8 PM / weekends 10–11 AM; YouTube weekdays 6–9 PM / weekends
  11 AM–2 PM; publish 1–2 hours *before* peak so the post is indexed when the peak hits.
  Source: https://cityandtalent.com/blogs/best-time-to-post-on-social-media-in-india
- Frequency floor: 3–7 Reels/week on IG; Shorts daily *if* repurposing existing vertical video (near-zero extra cost).
  Source: https://shreyasbagal.in/how-often-post-social-media
- Meme Adda's existing plan (2/day: 1 evergreen + 1 trend-jack, in the evening window) sits above the floor and
  matches the timing evidence. Consistency inside a fixed window beats volume spikes.

---

## 2. Formats — what actually travels in India right now

### 2a. Two-clip reaction — "connect the dots" (the founder's chosen format)
A setup clip (viral moment, news clip, everyday scene) cut to a TV/movie reaction clip as the punchline.
Evidence it is the dominant Indian meme grammar: the most-used Indian meme templates of 2025 are overwhelmingly
*reaction faces/lines from TV and film* — Jethalal's expressions (Taarak Mehta), Uday Shetty laughing (Welcome),
Hera Pheri trio planning, Ashneer Grover's "what's happening?" (Shark Tank India), Aman Gupta's folded arms.
Source: https://idiotic.media/most-used-meme-templates/
The evergreen well is Bollywood/TV dialogue: Hera Pheri alone sustains a dedicated project making a meme of
*every scene* in the film, documented by Know Your Meme; RVCJ's own list catalogues the dialogue-templates
("Jor jor se bolke sabko scheme bata de", "Control Uday, control", "Beta, tumse na ho payega"…).
Sources: https://knowyourmeme.com/memes/subcultures/hera-pheri-2000-film ·
https://www.newspointapp.com/english/trending/15-bollywood-dialogues-that-accidentally-became-meme-templates-rvcj/articleshow/1450482016a8520f311e9448699689ee5c6b2d10
The founder's own example (Pepsi/Coke setup → Punisher "no no no, wait wait wait") is this exact grammar.

### 2b. Template image memes (static + carousel)
Drake/Hera Pheri-style two-panel and image-macro templates — the IG feed staple of every mega page in §1, and the
cheapest possible news-jack (minutes from headline to post — the core of RVCJ's speed advantage; its template
library + consistent posting + collabs are the cited reasons it works:
http://thinkflowinsight.blogspot.com/). Already piloted by Meme Adda (launch carousel, memegen-built).

### 2c. POV / text-over-clip
One clip, the joke carried by a big caption ("POV: …"). This is the default Shorts/Reels grammar and the cheapest
video format to produce; it is also the format most exposed to the "low-value modification" rules in §2f when the
clip is someone else's and the caption is the *only* addition.

### 2d. Original skits / situational comedy
TVF-style scripted situational content scores the highest shareability (Hobo #2 above); @memesonlyz's positioning —
"original short-form comedy, built from scratch" — is the policy-safest end of the spectrum (already copied into
Meme Adda's brand pack). Slowest and most expensive to produce; not the launch format.

### 2e. Compilations
Historically the biggest raw-view format (clip channels in §1), and the format YouTube's reused-content rules
name explicitly (see §2f). Facts only; not Meme Adda's format.

### 2f. Copyright & policy facts for short TV/movie reaction clips (facts, not a recommendation)
The founder has decided the format; this is the true risk picture he asked the research to establish.

**YouTube — three separate systems, often confused:**
1. **Content ID claim (automated):** on a match, the rights holder's preset policy fires — *monetise* (ads run,
   revenue to the claimant), *track*, or *block* — and can differ by country. "Monetise is the most common policy
   applied to music claims." A claim "usually doesn't impact your channel or account" and is **not a strike**.
   Source (official): https://support.google.com/youtube/answer/6013276?hl=en&co=GENIE.Platform%3DDesktop
2. **Shorts-specific claim rule (official, same source):** for **Shorts of 1–3 minutes, a claimed video is blocked
   if there is an active claim, regardless of the holder's policy** — but "you will not receive a copyright strike
   for videos that contain active claims."
3. **Copyright strike (legal):** only a formal removal request creates a strike; **three strikes inside 90 days
   terminates the channel** (and linked channels). Claims redirect a video's revenue; strikes are the channel-killer.
   Source: https://chewbr.net/knowledge-bank/copyright-claim-vs-strike — which also warns that disputing a claim
   you have no rights to is the move that can escalate toward a strike; reading the notice type first is the discipline.
4. **Reused-content policy (separate from copyright, channel-level, decides YPP monetisation):** re-uploading
   others' content without significant transformation gets the *channel* rejected from the Partner Programme —
   and permission from the owner does **not** exempt a channel, because the test is whether the channel adds value.
   On the allowed side: "reaction videos that comment on the original" and edited footage with a new storyline/
   commentary. On the not-allowed side: "clips edited together with little narrative" and compilations of social
   media videos. Sources: https://cliptica.com/blog/youtube-reused-content-policy/ ·
   https://masterprompting.net/blog/youtube-ai-content-policy-reused-content-what-is-allowed
   YouTube tightened this on **15 July 2025**: YPP now explicitly targets mass-produced, repetitive and templated
   content; borrowed content must be *significantly altered*, and repetitive content must entertain or educate
   beyond views. Source: https://www.medianama.com/2025/07/223-youtube-monetisation-policy-repetitive-content/

**Instagram / Meta:**
- Rights-holder reports (DMCA) → post removed + a copyright strike on the account; repeat offences escalate.
  Source: https://abounaja.com/blog/report-copyright-infringement-on-instagram
- Meta's **Content Protection** (2025) scans FB + IG for reposts of enrolled creators' videos and lets the
  original creator track or block them, including partial matches.
  Source: https://routenote.com/blog/meta-content-protection-across-instagram-and-facebook/
- **Originality/recommendation rules (expanded Oct 2026):** unoriginal reposted content loses *recommendation*
  eligibility (Explore/suggested) — posts stay live for followers, but discovery is cut; eligibility recovers on a
  rolling 30-day window once most posts qualify as original; credit/watermarks do **not** make a repost original —
  a *material edit* is required. Sources: https://thevergetoday.pages.dev/news/920999/instagram-says-it-doesnt-want-your-tweet-round-ups ·
  https://futuretweets.com/instagram-repost-crackdown-30-day-rule-2026/
- Meta's own "unoriginal" list (Facebook side, Mar 2026) names **borders, inserted captions and speed changes as
  low-value modifications**, and lists "stitching several clips together" and "reacting only with facial
  expressions" as unoriginal patterns; consequences are reduced distribution, non-recommendable status, and
  demonetisation for repeat offenders. Source: https://cut.pro/en/blog/reposts-dont-pay-x-meta-youtube-2026

**How big channels actually handle it (observed practice, from the sources above):**
- They treat Content ID claims as a cost of doing business: most film/music owners choose *monetise/track*, so
  the video stays up and earns for the claimant while the channel keeps the audience growth (the views in §1 are
  accumulated under exactly this regime).
- They keep borrowed segments short, subordinate to their own edit — own setup, own captions carrying a narrative,
  own branding — which is also what moves a video from "clips edited together with little narrative" toward
  "reaction with commentary" on YouTube's allowed list, and toward "materially edited" on Meta's.
- Media-house pages (RVCJ class) lean on template/original production for most volume and use scene clips
  selectively, so no single claim can hurt the page.
**Net risk picture for Meme Adda's format:** reach risk is low (claims rarely remove; IG's penalty is lost
recommendation, recoverable), monetisation risk on the *specific claimed videos* is high (revenue follows the
claimant), and channel-existential risk concentrates in two places — formal strikes (3-in-90-days) and a
channel-level reused-content YPP rejection if the channel ever reads as pure clip-stitching with no added value.
Both are managed by production discipline (own setups, narrative captions, template/original majority), not by
avoiding the format.

---

## 3. Trend sourcing — the meme equivalent of Patna Pulse's RSS watch

**Where trends surface first (evidence):**
- A web-scale academic study (ACM, 2022) that traced image memes back through copies found **most image memes
  are first published on Reddit, then spread to other platforms** — meme origin is centralised, not peripheral.
  Sources: https://techxplore.com/news/2022-04-diffusion-image-memes-online.amp ·
  https://www.scienceaq.com/Article/Electronics/139656.html
- A working trend-tracker's stated method (viralmeme.ai): monitor **TikTok, Instagram, YouTube, X and Reddit**,
  cross-check **Know Your Meme's newsfeed** and **rising Google searches (Google Trends)**, then rank.
  Source: https://viralmeme.ai/trending
- Template half-life is now ~**48 hours** before a format is replaced or absorbed — trend-jacking is a
  same-day discipline, not a weekly one. Source:
  https://www.outreachplus.com/publications/7d37af/bba76f/trending-meme-templates-2025.pdf

**The India/Desi watch list (pipeline inputs):**
1. **Reddit (origin layer):** r/IndianDankMemes — its community describes itself as India's biggest meme
   subreddit (its official Discord alone is ~19.8K members:
   https://discord.com/servers/r-endiandankmemes-940583485230440538); plus r/dankmemes + r/memes for global
   formats 1–2 days before they localise, and Desi humour subs as configured sources for `watch.py`.
2. **X (velocity layer):** India trending list + the big Desi meme accounts; X is where a Reddit format gets its
   Hinglish caption and becomes quotable.
3. **YouTube IN (demand layer):** Trending page + Shorts feed; YouTube India's own trend cycle is driven by film
   releases, cricket (IPL/Asia Cup) and viral sounds (§1) — the release/match calendar is a predictable trend feed.
4. **Google Trends IN (confirmation layer):** "Trending now" for India + rising queries on a format's name —
   the same signal viralmeme.ai uses to rank; catches a trend on the way up, not at peak.
5. **Know Your Meme (provenance layer):** confirms a format's origin, name and template — the difference between
   riding a format and misreading a one-off post.
6. **Internal layer (our unfair advantage):** Patna Pulse's own `data.json` — Bihar/Patna headlines are a
   ready-made local trend feed for the reactive slot (the RVCJ news→meme play, but Patna-first, where no mega
   page competes).

**The pipeline this enables — `watch.py`, the meme `generate.py`:**
Run 2×/day (morning + late afternoon, ahead of the 7–9 PM posting window): pull Reddit hot/rising (PRAW),
Google Trends IN, YouTube trending, and hand-picked items in `curated.json` (the founder's scenes land here,
exactly like Patna's hand-verified stories); cluster by format/topic; score **heat = number of independent
sources carrying it (3+ = 🔥 verified trend, 2 = rising, 1 = single/watch)** — the genuineness score, verbatim;
write `trends.json` → the GitHub dashboard (§5). A 48-hour half-life means the dashboard's job is triage:
anything "verified" today is tomorrow's stale.

---

## 4. GitHub tooling shortlist (for the INSTALL phase — nothing installed yet)

Every repo below was opened and verified on GitHub on 2026-10-23 (stars/license as of that date).
VM reality check (measured locally): ffmpeg 8.1.2 and Pillow already installed; **faster-whisper 1.2.1 already
installed**; Python 3.12.3; ~18 GB disk free; **<1 GB RAM available and no Docker** — heavy services cannot run here yet.

| # | Repo | ★ / License | What it does for Meme Adda | Install cost on this VM | Verdict |
|---|------|-------------|----------------------------|--------------------------|---------|
| 1 | **yt-dlp/yt-dlp** https://github.com/yt-dlp/yt-dlp | ~200.5K / Unlicense | Fetch scene clips + metadata from YouTube/IG/X links (founder's scenes, trend examples); pull trending/shorts metadata for `watch.py` | One pip package or single binary; trivial | **INSTALL** |
| 2 | **Zulko/moviepy** https://github.com/Zulko/moviepy | ~15.0K / MIT | The two-clip assembler in Python (concat setup+reaction, 9:16 crop, text overlays, audio mix) — same language as the whole Patna pipeline | `pip install moviepy`; uses the ffmpeg already present | **INSTALL** |
| 3 | **jacebrowning/memegen** https://github.com/jacebrowning/memegen | ~1.8K / MIT | Self-hosted version of the memegen.link API the pilot already used — removes the external dependency and lets us add **our own Desi templates** (Hera Pheri/Jethalal frames) as first-class templates | Python web app, moderate (or keep using the hosted API on day 1) | **INSTALL** (local instance in GitHub phase) |
| 4 | **praw-dev/praw** https://github.com/praw-dev/praw | ~4.3K / BSD-2 | Reddit API wrapper — the origin-layer feed for `watch.py` (hot/rising on configured subs) | `pip install praw`; needs a free Reddit app credential (founder creates it — his hands, like other sign-ins) | **INSTALL** |
| 5 | **openai/whisper** https://github.com/openai/whisper | ~111.1K / MIT | Clip transcription → caption drafts + a searchable scene index | **Already covered**: faster-whisper 1.2.1 (same models) is installed on this VM | **INSTALL — already present, skip duplicate** |
| 6 | **m-bain/whisperX** https://github.com/m-bain/whisperX | ~24.8K / BSD-2 | Word-level timestamps → karaoke-style burned captions timed to the punchline | Heavy PyTorch stack (several GB of the 18 GB free); CPU-only here, but our clips are <60 s | **TRIAL** (after the core pipeline works) |
| 7 | **D3vd/Meme_Api** https://github.com/D3vd/Meme_Api | ~0.9K / MIT | Ready-made Reddit-meme JSON API with per-subreddit endpoints (e.g. `/gimme/IndianDankMemes`) + upvotes — a zero-credential prototype of the trend feed (hosted at meme-api.com) | Zero if we call the hosted API; self-host is a small Go service | **TRIAL** (hosted API for the dashboard prototype) |
| 8 | **sansan0/TrendRadar** https://github.com/sansan0/TrendRadar | ~63.1K / GPL-3.0 | Multi-platform hot-list aggregator + RSS + keyword filters + digest pages — **but its sources are Chinese platforms** (Weibo/Zhihu/Bilibili via newsnow); no Reddit/X/YouTube-IN | Docker-oriented; GPL-3.0 | **TRIAL as architecture reference only** — copy the config/digest pattern, not the data |
| 9 | **GeneralMills/pytrends** https://github.com/GeneralMills/pytrends | ~3.7K / other | Unofficial Google Trends API | **Repo is ARCHIVED** (read-only, seeking maintainers) | **SKIP** — use Google Trends' own India trending RSS inside `watch.py` instead |
| 10 | **gitroomhq/postiz-app** https://github.com/gitroomhq/postiz-app | ~37.3K / AGPL-3.0 (stars per https://leadlabhq.com/news/postiz-free-social-scheduler/) | Full social scheduler + analytics for 30+ networks, incl. an MCP server agents can drive | Self-host needs PostgreSQL + Redis + Temporal and ≥2 GB RAM (https://omnisocials.com/postiz-alternative) — **cannot run on this VM today**; also duplicates our working instagram-cli + YouTube uploader, and has no read-back verification | **SKIP for this VM** (revisit only if a bigger host appears) |

Notes: ffmpeg itself (system, v8.1.2) stays the fallback assembler — MoviePy is convenience, not a dependency
we're hostage to. No analytics tool is needed at launch: YouTube Studio + IG Insights + our own `state/` logs
cover a 2-post/day channel; Postiz-class tooling only earns its keep at multi-channel scale.

---

## 5. GitHub foundation design — the Patna Pulse mapping

**Repo:** `niteshlhsnda-droid/meme-adda` → dashboard at https://niteshlhsnda-droid.github.io/meme-adda/
(same naming pattern as `patna-pulse`). Deliberately built **without GitHub Actions**: publishing is GitHub-API
PUTs + static Pages serving, exactly like Patna Pulse — so it does not depend on Actions at all.

```
meme-adda/
├── README.md                  # what it is, dashboard link, format rules + §2f risk rules in one page
├── index.html / styles.css / app.js
│                              # trend dashboard — renders trends.json (Patna's index/app.js pattern)
├── trends.json                # OUTPUT of watch.py (the data.json role): today's trends, heat, sources
├── curated.json               # hand-picked trends + founder's scene tips (Patna's curated.json role)
├── watch.py                   # trend collector: Reddit (PRAW) + Google Trends IN RSS + YouTube trending
│                              #   + curated.json → trends.json; heat = independent-source count
├── templates/
│   ├── templates.json         # template DB: id, name, origin (film/show), scene ref, file, last-used,
│                              #   use-count, rights note (claim-prone? evergreen?)
│   ├── frames/                # template stills/clips + a source log for every file
│   └── memegen/               # Desi template additions for the local memegen instance
├── tools/
│   ├── fetch_clip.py          # yt-dlp wrapper: URL + timestamps → build dir, logs provenance
│   ├── build_meme.py          # two-clip assembler (MoviePy/ffmpeg): setup + reaction + captions + hook
│                              #   frame (the assemble_news_reel.py role)
│   ├── make_captions.py       # faster-whisper → timed captions (SRT/ASS) for burning in
│   ├── publish_trends.py      # PUT trends.json + assets via GitHub API (the publish_data_json.py role)
│   └── post_and_verify.py     # post via instagram-cli / YouTube uploader → READ-BACK verify
│                              #   (posts --limit 10, caption match) before anything is marked posted
├── state/
│   ├── posted.json            # posted meme ids — the dedupe list (posted_story_ids.json role)
│   ├── used_templates.json    # template rotation + cooldown (no template repeats inside N days)
│   └── queue.json             # production queue: trend → scripted → built → posted
├── build/YYYY-MM-DD/          # per-day production dirs — never /tmp (standing workspace rule)
├── research/                  # this report + weekly ecosystem/format notes
└── channel-setup.md           # brand pack — single source of truth (moved from meme-pilot)
```

**Daily workflow it enables:** morning `watch.py` → dashboard shows the day's verified/rising trends →
pick 2 (1 evergreen template + 1 trend-jack, the standing 70/30) → scenes arrive via `curated.json` /
`fetch_clip.py` with provenance logged → `build_meme.py` assembles, frames eyeballed (visual-QC rule) →
`post_and_verify.py` posts IG Reel + YT Short inside the 7–9 PM IST window → `state/` updated **only after
read-back** → weekly analytics + format notes appended under `research/`.

---

## (a) Install shortlist — ranked
1. **yt-dlp** — clip/metadata fetching (install)
2. **MoviePy** — two-clip assembly (install)
3. **memegen (local)** — template engine + Desi template DB (install)
4. **PRAW** — Reddit trend watch (install; needs founder's free Reddit app credential)
5. **Whisper** — already present as faster-whisper; no action
6. **WhisperX** — trial, for word-timed captions
7. **Meme_Api (hosted)** — trial, dashboard-prototype trend feed
8. **TrendRadar** — trial as design reference only
9. **pytrends** — skip (archived)
10. **Postiz** — skip on this VM (too heavy; duplicates working posters)

## (b) Proposed repo structure
`niteshlhsnda-droid/meme-adda` — `watch.py` + `trends.json` + `curated.json` (research layer, Patna's
generate.py/data.json pair) → static dashboard (`index.html`/`app.js`, Pages) → `templates/` (template DB) →
`tools/` (fetch, build, captions, publish, post-and-verify) → `state/` (posted/used/queue dedupe) →
`build/YYYY-MM-DD/` (production) → `research/` + `channel-setup.md`. Full tree in §5.

## (c) Exact next steps, in order
1. **RESEARCH — done** (this report). Founder reads it and confirms: format weighting (two-clip majority vs
   template/original mix) and the §2f risk posture. No other phase starts before this.
2. **GITHUB:** create `niteshlhsnda-droid/meme-adda` with the §5 structure; dashboard skeleton rendering a
   sample `trends.json`; move `channel-setup.md` in; verify the Pages site loads.
3. **INSTALL:** yt-dlp → MoviePy → local memegen → PRAW, in that order, each smoke-tested against the real
   pipeline (fetch one clip, assemble one two-clip test from our own footage, render one template meme, pull
   one Reddit hot list). WhisperX/Meme_Api trials only after all four pass.
4. **PRODUCTION (last, only after 2–3 pass):** daily workflow from §5; week 1 at 1 post/day while dedupe +
   read-back prove out, then the full 2/day cadence in the 7–9 PM IST window.
