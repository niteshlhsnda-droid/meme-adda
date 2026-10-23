# MEME-PLAYBOOK.md — How Meme Adda makes memes: Trend × Scene

**The idea in one line:** a meme = a *trend* everyone is already feeling,
told through a *movie/TV scene* everyone already knows.
Two videos, connected — **the trend is the setup, the scene is the punchline.**

Founder's format ("connect the dots", set 2026-10-22). His example:
a Pepsi/Coke taste-test setup + The Punisher's *"No no no, wait wait wait"*
reaction. That exact pairing is Sample 1 below.

## Why scenes beat static templates

- **Recognition in under 2 seconds.** The audience has seen the scene; the
  face alone delivers the emotion before a single word is read. A static
  template makes the viewer *read* the joke — a scene makes them *feel* it.
- **Emotion is acted, not described.** Baburao's confusion, Uday's panic,
  Jethalal's frustration are performances honed over decades of reruns.
  No caption we write outperforms Paresh Rawal's face.
- **The scene carries sound.** Dialogue audio is half the meme — the line
  is already in the audience's head, so the clip lands even muted (the
  face) and doubles when heard (the dialogue).
- **Trends give it a expiry-proof hook.** Evergreen scenes + this week's
  trend = a meme that feels brand-new and instantly familiar at once.

## The method — step by step

### 1. Spot the trend
`watch.py` builds `trends.json` from three layers:
- **Google Trends IN** (confirmation layer — what India is searching now),
- **Reddit via PRAW** (origin layer — where Indian memes are born;
  goes live once Reddit approves the app),
- **curated seeds** (`curated.json` — hand-picked beats + the founder's
  scene tips) and seasonal context (festivals, counting days, salary day,
  exams, cricket).

Heat = independent-source count: 3+ = 🔥 verified, 2 = rising, 1 = watch.
Pick trends with a *feeling* attached — panic, greed, relief, frustration,
overconfidence. A trend without an emotion has no scene to pair with.

### 2. Name the trend's core emotion in one line
Before touching any clip, write the beat in ≤8 words:
*"New trader sees first red candle — panic."*
*"Counting day — everyone has already 'won'."*
*"Salary + Diwali sale — wallet loses control."*
If you can't name the emotion, the trend isn't meme-ready yet.

### 3. Match the scene — the scene bank
Pick the iconic moment whose *acted emotion* is that beat. Starter bank:

| Emotion / beat | Scene | The exact beat it serves |
|---|---|---|
| Confusion, "yeh kya ho raha hai" | Baburao (Hera Pheri) — phone/plan confusion | Any system, app or rule the public can't parse |
| Secret scheme exposed | Hera Pheri — *"Jor jor se bolke sabko scheme bata de"* | Leaks, announcements, someone saying the quiet part loud |
| Group scheming / hisaab-kitab | Hera Pheri trio planning huddle | Elections, counting day, office politics, family planning |
| Uncontrolled excitement / panic-buying | Uday Shetty (Welcome) — *"Control Uday, control"* | Sales, salary day, market rallies, wedding season |
| Fraud-call / too-good offer energy | Majnu Bhai (Welcome) — painting & panic beats | Scams, offers, "limited period" anything |
| Swagger / threat / "apna time" | Munna Bhaiya (Mirzapur) — calm-menace lines | Comebacks, wins, exam results, boss energy |
| Bureaucratic exasperation | Panchayat — Sachiv ji / Pradhan pati sighs | Government offices, forms, queues, paperwork |
| Blind optimism against all logic | Rancho (3 Idiots) — *"Aal izz well"* | Exams, results, deadlines, jugaad fixes |
| Household frustration meltdown | Jethalal (Taarak Mehta) — outburst at Daya | Family WhatsApp forwards, festivals, bijli bill, guests |
| Full-power dramatic entry | Daya (CID) — door-break | Any "ab main aata hoon" arrival: Monday, boss, inspector |
| Loyal sidekick agreement | Circuit (Munna Bhai) — *"Bhai ne bola karne ka to karne ka"* | Friendship, jugaad partnerships, yes-man moments |
| Escalating panic denial | The Punisher — *"No no no, wait wait wait"* | Taste tests, results, weigh-ins — realisation dawning |
| Dismissive expert rant | Ashneer Grover (Shark Tank India) — *"yeh kya ho raha hai"* | Wahiyaat products, bad ideas, market FOMO |

Rules of the bank: one scene = one beat (don't stretch a confusion face
into a celebration); rotate scenes (log usage in `state/used_templates.json`);
when a scene's beat is spent, retire it for a month.

### 4. Build — the anatomy of every Meme Adda video
9:16, 1080×1920, total **8–20 seconds**:

1. **Setup (1.5–3.5s)** — the trend, as a bold Hinglish text card
   (or a short own/setup clip). One line, readable at thumbnail size.
   This is the hook: if the setup doesn't land in <2s, nothing else matters.
2. **Reaction scene (3–8s)** — the matched scene clip, **scene audio kept**.
   Landscape sources get the blur-pad treatment (sharp centre, blurred
   fill) — never stretch, never crop a face off.
3. **Punchline caption** — one Hinglish line overlaid on the reaction,
   top band, **never covering the face**. The caption names the joke;
   the face delivers it.
4. **Brand end-frame (~1.5s)** — laughing-kulhad mascot + MEME ADDA +
   handles. Every video ends as ours.

### 5. Production recipe (installed stack)
- **Fetch:** `yt-dlp` — official/clip uploads preferred (Prime Video India,
  Shemaroo, Netflix India, SET/SAB official channels) over template
  compilations. VM quirks, learned 2026-10-23: always pass
  `--no-check-certificates` (proxy cert) and, if YouTube throws the
  "not a bot" wall, `--extractor-args "youtube:player_client=android"`.
  Log every source in the build dir (provenance is not optional).
- **Assemble:** MoviePy / ffmpeg via `tools/build_meme.py` pattern.
  ffmpeg 8.x on this box: concat video and audio in **separate** filter
  runs, then mux `-c copy` (the joint concat filtergraph fails).
  H.264 + AAC, loudnorm the scene audio to ≈ −15 LUFS, silent setup/end
  segments get an AAC bed so the file always has audio.
- **Statics:** local memegen (offline) for image memes/carousels only —
  video is the primary format; a static is a fallback, never the plan.
- **Captions:** Hinglish, Latin script, ≤2 lines, bold — legible on a
  phone thumbnail without zooming.

### 6. QC checklist (every video, no exceptions)
- [ ] Hook lands in <2s (setup readable on first frame)
- [ ] Reaction face fully visible, unobstructed, caption clear of it
- [ ] Caption legible at thumbnail size
- [ ] Scene audio present and intelligible (file has AAC; check mean volume)
- [ ] Total length ≤20s; 1080×1920; H.264 + AAC verified with ffprobe
- [ ] One joke, one emotion — if it needs explaining, it fails
- [ ] Frames eyeballed (setup / reaction / end) before anything ships

### 7. Rights & safety
- **Short, transformative clips only** — a few seconds of a scene, inside
  our own edit, carrying a new joke. Never full scenes, never episodes,
  never a clip re-uploaded as-is.
- **Credit in the DESCRIPTION, never on the frame** (founder rule,
  2026-10-23): the post caption/description names the film/show and the
  clip source. Frames stay clean.
- **Never repost another creator's finished meme.** Their edit is their
  work; we source the *scene*, we make our own meme.
- Meme Adda owns the setup, the edit, the captions and the brand frame —
  the borrowed scene stays subordinate to our edit (see README's format +
  risk rules; Content ID claims are a cost of business, strikes are what
  the discipline above exists to avoid).

## Samples — 2026-10-23 (founder review set, not posted)

Built in `samples/2026-10-23/` (this workspace; details + QC in
`samples/2026-10-23/SAMPLES.md`):

| # | File | Concept |
|---|---|---|
| 1 | `samples/2026-10-23/sample-01-pepsi-coke-punisher.mp4` | Pepsi vs Coke blind taste-test bravado → Punisher's "No no no… WAIT WAIT WAIT" meltdown (the founder's canonical example) |
| 2 | `samples/2026-10-23/sample-02-stock-market-ashneer.mp4` | "Upstox login" trending at market open (today's Google Trends IN cluster) → Ashneer Grover's "yeh kya ho raha hai?!" rant |
| 3 | `samples/2026-10-23/sample-03-mlc-counting-herapheri.mp4` | Bihar MLC counting, 27 Oct → Hera Pheri trio's scheming huddle: every party has already calculated its win |
| 4 | `samples/2026-10-23/sample-04-chhath-prep-jethalal.mp4` | Chhath prep's endless kaam-list (13–16 Nov) → Jethalal's wide-eyed outburst |
| 5 | `samples/2026-10-23/sample-05-diwali-sale-uday.mp4` | Salary credited + Diwali sale live (8 Nov) → Uday's boat rant while the wallet screams "Control Uday, control!" |

*Playbook set 2026-10-23 on the founder's order. Method first, production
second — the Patna Pulse way.*
