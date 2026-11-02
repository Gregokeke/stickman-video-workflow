# Fasting — Self Recycling

Complete editable HyperFrames/GSAP project for the supplied fasting/autophagy narration. Vertical 1080×1920, 30fps, 82.3333 seconds. The packaged MP4 is byte-identical to the separately delivered render.

61 distinct principal PNG illustrations across 69 appearances: 38 new built-in ImageGen illustrations/edits and 23 exact phrase-matching assets from the approved Last Meal Tonight and Eggs projects. All generated principal artwork uses actual alpha transparency. Main actors are expressive dressed stickmen with round heads and simple limbs; visible internal anatomy uses plain unclothed cartoon silhouettes. Prompt requests and exact reuse provenance are included.

The original 85.0808-second supplied ElevenLabs recording is retained. Silence-only cuts reduce it to 81.92494 seconds; the opening keeps 70ms of silence on either edge, later cuts 90ms. No words are rewritten, no speech regenerated, no time stretch or pitch shift. One local word-timestamp pass was made after snapping. Original audio, exact cut intervals, snapped narration, effects stem and final mix are included. The video has 46 exact phrase caption groups matching the established reference style.

## Open and edit

Unzip the entire folder. Requires Node22+, Python3.11+ and FFmpeg. Run `npm install` and `python3 -m pip install -r requirements.txt`.

- `storyboard.json` is the canonical timing/layout/connected-motion source.
- `captions.json` holds exact wording and phrase timings; `words.json` preserves word timing.
- `animation.js` defines independent entry, pose and handoff transforms, directional moves, behind emergence, foreground crops and registered cane retargets.
- `micro-explanations.*` contains persistent illustrative gauges, switch changes, division separation and small attached repair/negation changes.
- Run `python3 build.py` after source edits.
- `npx hyperframes preview` opens the editable project studio.
- `node render.mjs` renders deterministic 30fps frames and exports H264/AAC MP4. Browser setup is automatic on Linux x86_64; set CHROME_PATH on other systems.
- To rebuild the exact snapped narration, run `python3 rebuild_audio.py`; then `python3 mix_audio.py` rebuilds the current sound mix.

The main images remain in assets/graphics; fonts, GSAP, source sound clips and narration are bundled. There are no required remote asset URLs. A large PNG can trigger HyperFrames' inline-size warning; the actual PNG is bundled and the verified local renderer loads it directly.

## Choreography and accuracy

Phrase-gated arrivals distinguish food refusal, energy input, glucose/insulin drops, the survival switch, autophagy, senescent-cell metaphors, inflammation, cellular fragments, amino acids, fuel, and repair. Related subjects remain only while relevant and reposition as the next subject enters. No illustration reposition is counted as a new distinct asset.

The brain-fog image has an identity-preserving edited counterpart with the cloud removed and refreshed expression; its state transition is registered at the same position and size. The retired-cell/roommate jokes use specific expressive acting. Gauge shells stay fixed while fills descend; the instructor tracks the changing boundary. The stem-cell instructor changes facing/side when pointing at the worn-out cell. Cane tips are measured against screen targets in production/pointer-audit.json.

Biological images are explanatory schematics, not exact scale/chemistry or measured clinical results. The supplied narration's wording is preserved. No fasting-duration recommendation, patient reading, fabricated percentage, or additional treatment claim was introduced. Gauges have no numerical clinical scale and are labeled illustrative.

## Sound and validation

61 sound cues from 18 supplied sound-pack clips, with aligned attacks, full tails, restrained fine-detail cues and protected narration. No music. Master targets about -16LUFS/-2dBTP. See sound-cues.json and production/audio-mastering.json.

Production reports include runtime validation, layout inspection, lint findings, pointer registration, sampled-frame review, encoded-audio measurement, full-decode/frame-count verification and a manifest of every packaged file. Lint's structural nested-track/media-discovery warnings are retained; runtime and sampled layout checks pass. Intentional lower-body crops and transient entrance/transition overflow are marked.
