# When He Goes Quiet — editable HyperFrames project

Vertical 1080 × 1920, 30 fps. Supplied deep male narration, locally tightened from 79.39 to 68.78 seconds. Composition includes a short tail, total 68.983 seconds. No new voice generation. No music.

## Open and render

Install Node.js 22+ and FFmpeg. From this folder:

```bash
npm ci
npx hyperframes telemetry disable
npx hyperframes browser ensure
npx hyperframes preview
```

Use the Studio URL printed by the preview command. Render the edit:

```bash
npx hyperframes render --fps 30 --quality high --output renders/When-He-Goes-Quiet.mp4
```

`index.html` is the editable composition. Its registered `main` GSAP timeline controls all motion. `DESIGN.md` defines the approved red graphic style, white field with inward edge shadows, fluid movement and still holds. Captions are editable HTML, timed to the actual recording.

## Included material

- Twenty-two ImageGen illustrations, generated using three supplied style references; a duplicate of the generous man is used as his former self in the ending.
- Original voice MP3; trimmed narration, separate effects track and final mix WAVs.
- Word timestamps, caption timing, exact silence edits, sound cue map, source manifest, and 27-beat storyboard.
- Three visual references and sound-effect credits.
- `build.py` rebuilds captions, sound mix and HTML; requires Python 3, NumPy and FFmpeg. Run `python3 build.py` from this folder after changing its choreography or captions.
- `prepare_audio.py` optionally reproduces trimming and word timestamps from the original recording; it additionally requires faster-whisper and its base.en model. Existing WAV and timestamp files are complete and ready to use without transcription.

## Creative notes

Each illustration is tied to a specific spoken metaphor: mute, wall, bare-minimum affection, false peace, funeral for feelings, emotional depletion, scraps, lost favors, lost check-ins, canyon and the final couch. The narration is retained exactly, including the male subject. Small speech bubbles and a crossed suitcase are minor code-drawn accents; the calendar and all main illustrations are generated. All main characters and props are generated bitmap artwork.

Scenes deliberately glide, reposition and overlap into still holds. There is no bounce or continuous hovering. The ending holds his physical presence while the earlier loving version recedes. All effects correspond to motion, time, a notification or a narrated emotional turn.

Transition refinement: ordinary outgoing illustrations start fading about 40 ms after the next illustration enters. The final couch/former-self overlay retains its original upward movement and fade timing.
