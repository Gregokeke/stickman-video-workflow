# Brainwave Besties

An86.23-second vertical stickman motion-graphics video based on the supplied K.V.Hagen narration. 1080×1920,30fps,H.264/AAC. The exact delivered MP4 is included in `renders/Brainwave-Besties.mp4`.

60 distinct original generated illustrations are actually used, plus3 approved instructor poses. Reframing and native diagram accents do not count toward the60. There are62 exact caption phrases and80 motivated effects cues; no music.

## Edit and preview

Requirements: Node22+,Python3,FFmpeg/ffprobe and compatible Chrome/Chromium. All images, fonts, GSAP, voice and sound sources are local; no generation credentials are required.

```sh
npm ci
python3 -m pip install -r requirements.txt
python3 build.py
npm run preview
```

The preview command prints the correct local Studio address. `index.html` is source, not a hosted preview link.

`storyboard.json` is the authoritative timing/layout source. Edit the actual artwork placements, moves and cane targets there. `captions.json` holds exact phrase captions. `animation.js` handles arrivals, connected moves and clean early fades. `micro.js` constructs independent, source-coordinate-registered display overlays. They move with their generated principal art, including during scale/repositioning. `DESIGN.md` defines the palette, typography and style.

## Render

On Linux, the locked browser dependency can be extracted with `npm run setup-browser`. On another platform set `CHROME_PATH` to a compatible local Chrome binary.

```sh
npm run setup-browser
python3 build.py
node render.mjs
python3 verify_audio.py
```

The deterministic renderer seeks the registered GSAP timeline for all2587frames, encodes CRF16 H.264/yuv420p and192kb/s AAC, checks the full audio-master length, and fully decodes the output. The audio verification compares every active narration window through the ending against the complete master.

## Narration and sound

The original89.54777-second recording is preserved in `assets/audio/source-narration.mp3`.16 genuine quiet-gap edits produce85.15442seconds of narration, with70ms detected-boundary tails and25ms protected word margins. No speech rate change, added pause or replacement voice take. `prepare_audio.py` and `audio-edits.json` preserve the edit. `source-words.json` and `words.json` retain source and tightened alignment. Local transcription is optional for a future realignment; it is not required to render this version.

`assets/audio/narration.wav`, `effects.wav` and `mix.wav` are separate. Edit `sound-plan.json`, then run `python3 mix_audio.py` to rebuild sound before rendering. Onsets use actual attack offsets; tails are retained.19 supplied source effects are used. Rights/provenance remain with the original owners; see `SFX-CREDITS.md` and `assets/sfx/Manifest.json`.

## Scientific illustration and review

Wave traces, highlighted regions and the download/rewiring metaphor are schematics, not fabricated trial data or authentic participant MRI/EEG recordings. The supplied narration is verbatim. See `production/SCIENTIFIC-NOTES.md` for primary sourcing and limits.

The source includes the actual style references attached to generation, the supplied platform red-zone canvas, approved instructor images and current workflow/motion/micro-explanation guides. Main artwork is original to this script; guide poses are explicitly identified reuse. This production builds from the approved fourth project's editable source and established reference studies, without claiming a new complete audiovisual review of unavailable earlier reference videos.

`production/` contains generation prompts/provenance, asset hashes, source-coordinate display registration, captions/timing schedules, mastering/export checks, pointer accuracy and held/transition overlap audits. The chamber padlock intentionally attaches to its door latch; incidental independent silhouette contact is corrected. The final video has no red-zone review overlay.
