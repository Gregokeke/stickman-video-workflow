# One Winner for Each Organ

Editable HyperFrames/GSAP composition using the supplied November1 ElevenLabs recording. Vertical 1080 × 1920, 30 fps, 135.7333 seconds. The separately delivered final MP4 and the MP4 inside the final ZIP are byte-identical.

80 distinct principal transparent PNGs across 89 appearances:71 newly generated principal illustrations (including 2 legibility replacements) and 9 exactly matched approved assets. Characters have thicker smooth tubular arms/legs, oversized round red heads, clear expressive eyes and simple contextual clothing; they remain cartoon stickmen rather than anatomical humans. Scientific diagrams and supplement bottles remain separate editable cutouts. Original generation prompts and refinement notes are included in production/.

The six chapters cover heart, eyes, kidneys, bones, liver, and muscles. Main props are aligned to the named words in the supplied narration. Related diagrams develop through connected movement and 21 behind-object emergence entrances, with varied lateral/diagonal/rising/foreground routes. Scientific pointers target actual screen coordinates and remain above diagrams. Deliberate micro changes include exact spoken study-number reveals, and a five-bar ATP battery losing four bars then replenishing them on the refuel phrase. Biological/molecule visuals are schematic, not exact chemistry or measured patient readings.

## Audio and captions

Original supplied take: 140.04246 seconds; careful silence-only snapping: 135.32375 seconds, plus final visual/audio tail.75–90ms edge protection, no speech regeneration, no speed/pitch changes. OriginalMP3, exact keep/cut intervals, snapped narration, effects stem, and final mix are bundled. One local word-timestamp pass; 74 curated phrase captions matching the fasting project's main typography. No separate lower-third subtitle track.

93 motivated cues from 10 supplied sound-pack clips, all full tails preserved. Main arrivals are prominent; detail cues are restrained. No background music. Master target around −16 LUFS / −2 dBTP. The supplied narration is preserved; its medical/study claims have not been independently fact-checked, and the production does not add new claims.

## Editing and rebuilding

Requires Node 22+, Python 3.11+, and FFmpeg. Unzip the entire folder and keep its internal layout.

1. Run `npm install` and `python3 -m pip install -r requirements.txt`.
2. Edit `storyboard.json` for canonical layout, timing and connected moves; `captions.json` for exact phrase text/timing; `animation.js` for routes and handoffs; `micro-explanations.*` for attached data motion.
3. Run `python3 build.py` after edits. `index.html` is generated from those sources. `npx hyperframes preview` opens the composition.
4. `node render.mjs` renders deterministic 30 fps H264/AAC MP4. Automatic Linux x86_64 browser setup; set CHROME_PATH to another Chromium installation where appropriate.
5. `python3 rebuild_audio.py` rebuilds the exact snapped narration from bundled original MP3 and kept intervals; `python3 mix_audio.py` rebuilds the current effects mix.
6. `node review.mjs`, `node audit-motion.mjs`, and `node audit-pointing.mjs` provide sampled visual and choreography checks. `package_project.py` verifies and packages the matching final render.

All consumed PNGs, fonts, GSAP, audio and sound sources are bundled. No external asset URLs are needed. Production reports retain runtime/layout/lint findings, settled-motion collision checks, pointer accuracy, sampled review, full decode/frame-count export checks, and file hashes. Intentional transition overflow and cane/target overlap are distinguished from settled illustration collisions. No infinite animations.
