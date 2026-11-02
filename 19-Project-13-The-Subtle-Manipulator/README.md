# The Subtle Manipulator

Finished psychology video, 1080×1920 at 30fps, 46.74 seconds. Supplied narration tightened from 52.271 to 46.066 seconds with protected silence-only edits; remaining time preserves the final sound tail. 35 distinct meaningful illustrations: 18 newly generated with the built-in ImageGen tool and 17 precisely reused approved images. Generation stopped when the Plus image limit was reported; no alternate image generator or code-drawn main artwork was substituted. Exact provenance and prompt set are included.

## Reproduce

Use Node.js 22+, FFmpeg and a usable Chrome Headless Shell. Run npm ci, then npx hyperframes browser ensure if required. Run python build.py only when changing captions, asset placements or moves; existing index.html is ready. Render with npx hyperframes render --fps 30 --quality high --workers 2 --output renders/The-Subtle-Manipulator.mp4. The package locks HyperFrames 0.8.181, the approved reference runtime. Python build requires Pillow. Source assets, fonts, GSAP, audio and timing are local; no external media is needed.

## Creative decisions

Art direction follows Quiet-People-Loyal-Friends-1 and Behind the Perfect Exterior. Motion follows Project 2 When He Goes Quiet Clean Fades: lateral/diagonal travel, early overlapping fades, firm holds, behind-to-front arrivals and center-to-side-to-center returns. No cane presenter or clinical micro-explainers. The guidance/mind sequence uses an open-handed person guiding the thinking subject across the canvas. No music.

36 motivated sound cues use 19 files from the supplied 72-effect pack, with manifest attack offsets, full decay tails, a separate effects stem and a speech-safe final mix. mix_audio.py rebuilds audio from the included source tracks and local sound manifest; NumPy and FFmpeg are needed. prepare_audio.py documents the original one-pass silence/transcription process; the approved words and narration are already included, so no transcription or speech generation is needed for a normal rebuild.

## Edit map

storyboard.json contains the 35 visible rectangles, phrase contexts and lifetimes. moves.json contains focused reframings and return moves. build.py generates index.html. Captions preserve every supplied word. audio-edits.json preserves the silence cut map. sound-cues.json preserves attacks and gains. asset-inventory.json records 35 unique image hashes. references includes real style references, the actual user red-zone canvas and the full workflow.

Review outputs, render caches and node_modules are omitted from the portable ZIP. The matching clean finished render is included under renders/.
