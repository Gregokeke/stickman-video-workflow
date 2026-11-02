# Protect Their Peace — editable video

One 1080 × 1920 portrait composition, 30 fps, 36.70 seconds. Uses the supplied deep male narration with 5.26 seconds of silent pauses removed, eight ImageGen illustrations on true alpha, phrase captions, and contextual effects.

## Re-render

Install Node.js 22 or newer, FFmpeg, and the pinned HyperFrames package with `npm install`. Run `npx hyperframes render . --fps 30 --quality high -o renders/Protect-Their-Peace.mp4`. HyperFrames provisions its browser; when using an existing Chromium set `HYPERFRAMES_BROWSER_PATH` to the executable. All composition media and GSAP are local.

`index.html` is ready to render without rebuilding. `build.py` regenerates it and the mix; requires Python 3, NumPy and FFmpeg (`python -m pip install numpy`). Edit its scene choreography and caption grouping there, then run `python build.py`. `words.json` timestamps already align to the trimmed narration, so do not transcribe or cut it again.

`prepare_audio.py` documents the original preparation step; supply your own source path if repeating it. `audio-edits.json` records the applied trims. `asset-sources.json` records original generated asset names; the authoritative copies are under `assets/`.

All principal characters and scene props were produced with ImageGen using three supplied red stick-figure references. Limited SVG is used for a strike accent only. Motion uses smooth non-overshooting easing and fixed holds. Background is white with inset edge shadows. Sound credits are in `SFX-CREDITS.md`.
