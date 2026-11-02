> **Compact lossless package:** Before previewing or editing, install the project dependencies below (including Pillow and FFmpeg), then run `python restore_assets.py` from this project folder. The bundled lossless files restore the original WAVs byte-for-byte and PNG pixels exactly at their original resolution. Existing source scripts/paths then work normally. The complete finished MP4 is already included and plays without restoration. Read `LOSSLESS-COMPRESSION.json` for checksums and provenance.

# Sugar · Two Weeks

70 used illustrations and props (60 newly generated, 10 accurate reuses), with 28 distinct source sounds and 77 action-timed cues.

Vertical red/black stickman explainer built in HyperFrames from the supplied ElevenLabs recording. 1080×1920, 30 fps. Supplied voice preserved; only detected genuine pauses shortened with protected boundaries. No new speech or music.

Open `index.html` through HyperFrames to edit or preview. All media is local and paths are relative. Captions, diagrams, choreography and target positions remain editable.

## Run

Requires Node.js 22+, Python 3 with NumPy/Pillow/SoundFile, FFmpeg/ffprobe and Chrome Headless Shell.

```bash
npm ci
npx hyperframes telemetry disable
npx hyperframes browser ensure
python3 build.py
npx hyperframes preview
```

`storyboard.json` controls artwork timing, layout, travel route, held poses and measured presenter targets. `captions.json` controls exact phrase captions. `animation.js` controls deterministic motion and schematic development. Run `python3 build.py` after editing those files.

```bash
npx hyperframes check --json
node audit-motion.mjs
node review.mjs
node render.mjs
```

`render.mjs` exports and fully decodes the H.264/AAC MP4. `CHROME_PATH` may select a local Chromium executable.

## Audio and artwork

`assets/audio/source-narration.mp3` is untouched. `narration.wav` is the snapped voice, `effects.wav` the separate sound stem, and `mix.wav` the mastered final mix. `audio-edits.json` preserves actual cut intervals and the retiming map. `source-words.json` and `words.json` preserve original and retimed alignment.

`asset-plan.json` records each illustration, phrase, source, prompt and approval when available. Unused draft artwork is excluded from the portable project. Read `production/USER-APPROVAL.md` for the held-prop clarification. Main illustrations were generated individually with ImageGen; accurate reuses come from the final Brain Overstimulation project.

`references/sfx-pack-manifest.json` contains the selected original pack records. All used source WAV clips are in `assets/sfx/`; `sound_design.py` rebuilds the mix from these local files. See `SFX-CREDITS.md` for provenance. The complete user-supplied effects pack is a separate deliverable from the earlier pack task.

Scientific shapes are schematic illustrations, not patient measurements. Entity references and production limitations are recorded in `production/SCIENTIFIC-ART-NOTES.md`. Original supplied narration wording is unchanged.

Revision: nineteen requested layout/timing/pointing fixes, including two upward-pointing variations. See production/REVISION-19.md. Registered cane tips are independently measured in audit-pointing.mjs.
