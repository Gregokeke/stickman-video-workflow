# Kiwi · Small Fruit, Big Attitude

114.6-second vertical film,1080×1920 at30fps.78 distinct used illustrations:76 new ImageGen illustrations/targeted edits and2 approved instructor poses. Duplicated kiwi boxer counts once, and repeated appearances/charts do not inflate the count.75 exact spoken caption phrases. Supplied narrator is authoritative: original120.1894s, silence-tightened112.82523s, with a short final effects tail. No music or regenerated speech.

## Play and edit

The matching final video is `renders/Kiwi-Small-Fruit-Big-Attitude.mp4`. The rendered film and source have the same timing.

Requirements: Node22+, Python3 with Pillow/NumPy/SoundFile, FFmpeg/ffprobe and an installed Chromium/Chrome Headless Shell.

```bash
npm ci
python3 -m pip install -r requirements.txt
python3 build.py
npm run preview
```

Set `CHROME_PATH` to your installed Chromium executable. Set `HYPERFRAMES_BROWSER_PATH` to the same executable for CLI checking.

```bash
npm run check
npm run render
```

The browser binary and node_modules are excluded. `browser-path.mjs` accepts the explicit browser path, local `.browser`, the HyperFrames cache or common system installation paths. The @sparticuz/chromium dependency also supplies compressed browser/font/shader files that can be extracted into a writable executable directory, as described in that package.

## Authoritative source

- `storyboard.json`/`.md`: final phrase cues, artwork bounds, connected moves, actual instructor tip targets and intentional crops.
- `build.py`: alpha-aware art fitting, measured cane transforms, phrase font fitting and generated index.html. It rejects reversed scene lifetimes.
- `animation.js`: deterministic registered timeline, travel/pose wrappers, lateral/diagonal/depth entries, center-to-side/back returns, finite emphasis and early opacity handoffs.
- `micro.html`/`.css`/`.js`: editable VS and slash, fiber units/water/colon flow, below-goal unit display, trial direction chart, time/gauge and endogenous sleep synthesis, fuel and protein-cleavage paths.
- `words.json`, `captions.json`, `script.txt`: final exact recorded wording and timing. `source-words.json`, `transcript.json`, `audio-edits.json` preserve original alignment and removed silence intervals.
- `sound-plan.json`, `sound-cues.json`, `mix_audio.py`: final action timings, attack offsets, individual gains and full effect tails. `assets/sfx` includes every used source plus its manifest.
- `render.mjs`: deterministic two-worker frame capture, CRF16 H.264/yuv420p, AAC192k, complete decode verification and refusal of shortened audio masters.
- `review.mjs`, `audit-safe.mjs`: held/moving frame review, pointer registration and actual supplied platform-mask checks.
- `asset-plan.json`, `asset-sources.json`: final used illustration purposes, generation descriptions/references and hashes. One image per prompt; no atlas/sprite/contact-sheet substitutes for generated art.
- `production`: final checks, scientific source notes, user-specific direction and craft study.

For a visual-only revision, edit the final JSON/micro source and run build/render. Do not rerun audio intake. `prepare_audio.py` and `transcribe.py` document optional original intake; transcription requires faster-whisper and its model. The saved alignment/narration are sufficient for normal editing.

## Current user-specific art rules

Micronutrients, molecules and cell illustrations are standalone without baked-in people. The approved man holding the heart is retained. The original blood-vessel design received a targeted edit to remove only its presenter, preserving the vessel/clot design. Large explanatory instructors are separate layers with measured cane tips, readable faces/grips and intentional lower-body crops.

The boxing comparison uses two instances of the ONE side-view kiwi boxer against the opposing orange, with a drawn diagonal VS slash, finite fighting gestures and a referee entering on “although”. The prayer figure and three-quarter open-front poop shrine are separate generated assets.

Full original supplied voiceover, tightened voice, separate effects and complete final mix are included. Audio mixing writes a staging file and verifies its exact frame count before atomically installing the final master. Export verifies the mix duration before muxing and checks decoded ending audio afterward. The documented source never pads a short voiceover to conceal an error.

Scientific drawings and nonspecific charts are schematic. The record's existing medical wording is preserved; no invented trial values or extra efficacy claims are added. Read production/SCIENTIFIC-NOTES.md for source context and interpretation limits.

## Precision revision

All24 requested fixes and the follow-up scissors exit are documented in `production/REVISION-24-FIXES.md`. The video is114.6s/3438frames. `revision-motion.js` adds seekable droplet travel and two separately clipped protein halves. The scissors sweep off-screen, the split halves remain, then the curved arrow draws before peptides appear. `audio-edits.json` records the0.6s inserted silence; every prior narration sample is retained. `micro.js` hides paths until their actual draw cue.

## Latest follow-up (authoritative)

Fruit-basket character raised90px and uniformly enlarged2.5%; other Vitamin E elements unchanged. Scissors and protein are on the same upper horizontal cutting axis. Scissors travel left-to-right and exit; protein splits into upper/lower halves. A C-curved arrow begins during cutting and leads to peptides. Cut-scene instructor removed. The previously added600ms pause has been removed and downstream word/caption/scene times restored.

Matching final export:114.6s,3438frames. The included render is the exact delivered video. Editable HTML/GSAP source and saved audio master reproduce its content and timing. The delivered export preserves unaffected video sections through a verified patch assembly; a full source re-render can differ in codec pixels. `mix_audio.py` records the earlier effect-mixing pipeline; the saved final master includes the silence splice and is authoritative for normal re-rendering.
