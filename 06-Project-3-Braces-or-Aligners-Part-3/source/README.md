# Braces or Aligners — Preparation for Adult Life, Part 3

Complete editable HyperFrames project for a42.633s,1080×1920,30fps stickman video. The supplied K. V. Hagen narration was gently tightened from44.931s to42.335s. No new voice generation, no music.23 distinct illustrations:21 new built-in ImageGen cutouts plus2 approved relevant presenter/series figures. The duration-based minimum is14; it is a floor, never a cap.

## Edit and reproduce

Install Node.js and FFmpeg/FFprobe. Install Python3 with NumPy and Pillow. From this folder, run `npm ci`, then `npm run build`. Open index.html using HyperFrames preview. It retains the audio element and registered paused GSAP timeline for editing.

Run `npm run render` to rebuild the source and export the full MP4. render.mjs resolves the HyperFrames Chrome binary, loads local images and fonts, seeks the registered composition at every1/30s, sends lossless PNG frames to FFmpeg, and muxes the approved mix. It uses H.264 CRF15 with two encoder threads, BT.709 and AAC192kbps. It decodes and probes the result before atomically adopting renders/Braces-or-Aligners-Part-3.mp4. This composition uses deterministic GSAP artwork/captions/paths; it contains no video textures, shaders or nested timelines requiring separate media synchronization. All assets/fonts/GSAP/audio are local. Telemetry is disabled in CLI invocations.

The optional prepare_audio.py script recreates the gentle silence pass and local word transcription. It requires faster-whisper and socksio. Final narration, words.json and the approved cuts are already included, so regeneration is unnecessary for an ordinary visual edit. Preserve real silence boundaries and consonant tails; never use transcript-estimated interword cutting. build.py corrects the orthodontic term “Aligners” from the recognizer's split homophone without changing the supplied recording.

## Included source

- assets/: all used illustrations, local font and GSAP, supplied narration, tightened narration, effects, final mix and approved sound-effect palette.
- references/: actual supplied source video, enlarged filter frame, three established style JPEGs and actual red-zone review PNG.
- asset-sources.json: every new ImageGen prompt plus precise approved-reuse provenance.
- reference-study.md: full concept inventory from the source, including exact **braces wialiska** effect/search spelling. The source's cats and typography are not copied into the output.
- build.py: explicit phrase-to-illustration timing, choreography, contextual holds, early fading exits, caption grouping, local progressive annotation traces and motivated sound cues.
- asset-layout.json: actual alpha bounds and CSS normalization. Source PNGs stay intact; silhouette-aware fitting keeps important characters readable.
- storyboard.md, production-notes.json and motion-events.json: context and timing documentation.
- Stickman-Animations-Workflow.md and OG-MOTION-STUDY.md: complete current style workflow and original connected-motion insights.
- review.mjs and audit.py:427 timeline samples at0.1s against the supplied red-zone canvas, with zero ordinary exceptions. The guide is used only for review, never burned into the clean MP4.
- verify-choreography.mjs: checks conflicting animation properties. Relevant results are included in safe-zone-report.json and choreography-review.json. Internal review screenshots, logs, drafts and node_modules are excluded.

Captions stay in the established upper position. Scenes use large heroes, moderately smaller supporting characters, deliberate vertical staggering and clear white gaps. The tray-fitting arrow connects the tray and teeth; the discomfort circle targets the tender tooth area; the negation traces over the aligner when the recording states its limitation. Annotation paths remain attached to their objects.

The video illustrates the supplied recording. It adds no personalized treatment prediction, diagnosis, clinical score, dose or app advertisement. The spoken timing qualifier stays attached to the three-year calendar; professional consultation remains a prominent specific scene.

The CLI layout inspector reports0 errors and0 warnings. Its one connector-orphan information message at27.001s concerns the fitting arrow: both endpoints are visible parts of the same generated PNG rather than separate DOM elements. The actual arrow is visually anchored in the tray-to-teeth gap.
