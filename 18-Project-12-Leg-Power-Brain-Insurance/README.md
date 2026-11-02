# Leg Power — Brain Insurance

Complete 1:53 portrait video: 1080 × 1920 at 30 fps, 76 distinct original illustrations across 77 appearances, 79 caption phrases and all 332 spoken words. The matching finished video is in `renders/Leg-Power-Brain-Insurance.mp4`.

The supplied voice is preserved. Only genuine silence was shortened, with protected word boundaries and no speech speed change or added internal pauses. The full 113-second master uses 83 motivated sound cues from 14 supplied effects, with no background music.

## Open and render

Requires Python 3, Node.js, npm, ffmpeg and ffprobe. From this folder:

```sh
pip install numpy soundfile Pillow
npm ci
npm run setup-browser
npm run build
npm run preview
npm run render
npm run verify
```

`index.html` contains the complete composition. `full_schedule.py` defines staging and phrase cues; `full-animation.js` defines deterministic movement, emergence, accents and precise instructor targeting. `build_full.py` creates the full HTML and caption data. Preview may require an initial HyperFrames CLI download. Browser binaries and node_modules are intentionally installed locally rather than bundled.

For layout review, run `npm run review`. To rebuild sound from supplied originals, run `npm run mix`. The existing word alignment and tightened narration are included; transcription is optional and unnecessary for normal editing/rendering. Rebuilding the original audio edit requires `prepare_audio.py`.

## Included sources and checks

All 76 original transparent PNGs are included without lossy recompression: 57 project-generated assets and 19 user-returned generated cutouts. Prompts/provenance, hashes, reference mappings, the original narration, audio edits, complete mix, effects, fonts, GSAP, captions and storyboard are retained. Approved instructor poses are reused references and do not inflate the original illustration count.

Related details emerge from visible source props and settle into separate positions. Instructor cane tips track actual moving targets. Full-frame visibility, alpha-aware layout, captions, image loading and encoded audio are checked. Reports are in `production/`; scientific interpretation notes and supplied-effect credits are also included.

`npm run package` creates the portable project ZIP and verifies that its embedded finished MP4 matches the standalone export byte-for-byte.
