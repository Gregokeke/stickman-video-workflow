# Bouncy UI — dimensional motion addendum

Revision: 30 October 2026. Read alongside `Bouncy-UI-Animation.md`, which contains the original reference inventory, detailed source timestamps and base motion recipes.

## What this revision changes

The original sample was a nine-second single-stage study. This revision is a 22-second, three-scene motion-graphics demonstration. It adds visible object depth, stronger spring response, longer connected movement, more deliberate lighting and a new third scene designed for this study.

The reference remains the guide for clock selection, falling interval tags and time-card entrances. The dimensional materials and the rhythm sculpture are creative extensions, not claims about how the source video was built.

## Scene plan

| Demo time | Scene | Main action |
| --- | --- | --- |
| 0–6.8 s | Pick your wake-up time | Rounded coral clock springs onto the stage, floats through a small change of orientation, resolves its digits to 8:00, rings, then receives two tumbling lavender interval tags. |
| 6.8–7.85 s | First transition | Incoming stage slides over the retained clock scene with acceleration and deceleration. |
| 7.85–13.7 s | Count back | Three thick time capsules cascade into place from alternating directions, retain their earlier rows and complete a highlighted result and mint badge. |
| 13.7–14.8 s | Second transition | A new stage moves over the completed cascade. |
| About 14.8–19.3 s | Find your own rhythm — original | FOCUS, REST and PLAY tokens assemble around a gold orb, glide through offset positions, then follow separate approach lanes into a vertical arrangement. |
| About 19.25–21.5 s | Original impact and resolution | The orb drops and rebounds. A delayed wave passes through the three docked tokens; a mint IN SYNC badge and small stars complete the action. |
| 21.5–22 s | Finish | Gentle final fade. |

This is a visual motion study. The times and labels are demonstration content, not medical recommendations.

## How the dimensional appearance is built

The project uses CSS 3D transforms and layered geometry, with SVG-free procedural interface construction and a locally bundled GSAP timeline. It is a dimensional UI treatment rather than a photorealistic 3D simulation.

### Thickness

Every clock case, capsule and rhythm token has a stack of rounded depth slices behind its front face. Slices sit two pixels apart along the local Z axis. The clock and rhythm tokens use 16 slices, while the time cards use 12 and the small tags use nine. Rotating the object reveals the darker sidewall rather than simply rotating a flat image.

### Perspective

Each graphic stage has a 1,700 px perspective distance. Objects enter with larger X/Y rotations and Z displacement, then settle into a gentler three-quarter pose. The front face, sidewall, clock dial and digits have distinct depth positions. Text travels with its parent object and finishes in a readable state.

Avoid aggressive perspective on small numerals. A large rotation may be useful during travel, but the selected time must hold near enough to the viewer to read comfortably.

### Material and light

The palette preserves the reference's navy, coral, lavender, gold and mint. Front faces use local directional shading, a bright upper edge and a darker lower edge. Sidewalls are darker versions of each material. The gold sphere has a concentrated upper-left highlight and a shaded lower-right edge.

The dial is inset into the coral case, with its own inner shadow and bright lip. Rounded alarm bells and supporting feet give the clock a more complete silhouette. The card faces remain simple enough that the time values retain first priority.

These object-level shading gradients are intentional in this revision. They replace the original demo's flat surfaces; they do not introduce a busy full-frame gradient.

### Contact shadows

The clock's stage shadow expands and darkens as the clock returns toward its resting height. The card stack has a softer, wider shadow. Shadows belong to the stage rather than being permanently attached to the object's outline. This helps communicate height and mass during rebounds.

## Motion changes

### Longer spring recovery

Main entrances now last roughly 1.05–1.35 seconds, depending on the object's role. They combine travel, perspective and angular movement. Smaller impacts use a shorter compression followed by a longer, damped recovery. This creates more bounce without forcing every element to oscillate continuously.

A representative main entrance uses `elastic.out(1, .52)` or a nearby tuned period. These are authored recipe values. They were not recovered from the reference project.

### Travel and settling

Clock movement includes a small lifted pose followed by a spring return. Card entrances alternate directions to make the cascade less repetitive. Their resting tilt is consistent, while each arrival has a stronger initial attitude. Small tags fall through depth, compress briefly at contact, lift and settle.

The resting pose remains important. Bounce should lead to a clear state, not delay or obscure it.

### Original third-scene choreography

The three tokens begin in distinct positions around a central orb. Their rotations and approach times differ slightly. As they dock, the side tokens use separate left and right lanes so their labels do not pass directly through the center token. The orb's impact occurs after the last docking motion. Its impulse is followed by a staggered downward-and-back wave through the stack and then the IN SYNC confirmation.

This scene is an original metaphor for finding a rhythm among activities. It is not copied from the supplied reference. The small orbit line is a visual guide, not an exact physical simulation.

### Transitions

The outgoing scene remains intact while the next solid stage sweeps over it. Each scene has an isolated stacking context, so a prior headline cannot remain above the incoming background. Explicit clip windows end each outgoing scene after the covering transition completes.

All animation is deterministic and can be evaluated at an arbitrary time on the paused root timeline. There are no infinite repeats, browser timers, live clocks or random event schedules.

## Reference clips in this package

These are excerpts of the user-supplied `1000002059.mp4`, with the original picture, watermark and source audio preserved. They are reference footage, not newly created demo scenes. Video and audio were re-encoded for frame-accurate trimming and common playback compatibility.

| File | Source range | Focus |
| --- | --- | --- |
| `reference-clips/01-Opening-Clock-and-Text.mp4` | 00:00.00–00:05.35 | Opening headline scale, small ringing clock and supporting indicators. |
| `reference-clips/02-Clock-and-Falling-Tags.mp4` | 00:36.10–00:40.75 | Time selection on the alarm clock, ringing marks, tumbling subtraction tags and the counting-back arrow. |
| `reference-clips/03-Time-Card-Cascade-and-Selection.mp4` | 00:41.55–00:51.70 | Tilted first-card entry, progressive time stack, selected gold rows and small result tag. |

`Bouncy-Reference-Compilation.mp4` joins those excerpts in that order, using direct cuts between excerpts. It does not interpolate missing footage, add music or alter the reference's speed. Small differences of a video frame or audio packet from the requested durations are normal in encoded media. The individual clips are provided as well as the compilation.

## Project structure

- `Bouncy-UI-Animation.md`: the complete original reference study.
- `Bouncy-UI-3D-Addendum.md`: this revision guide.
- `Bouncy-UI-3D-Demo.mp4`: improved three-scene render.
- `Bouncy-Reference-Compilation.mp4`: joined source excerpts.
- `reference-clips/`: all three separate reference excerpts.
- `editable-project/`: HTML composition, design specification, bundled GSAP, font and original synthesized effects.
- `previous-sample/Bouncy-UI-Demo.mp4`: the original nine-second sample for before/after comparison.
- `verification/`: the composition check report and output metadata.

## Editing and reproduction

The editable project includes all visual dependencies locally. Node 22 or newer, FFmpeg and the HyperFrames browser are required for re-rendering. The scripts pin HyperFrames 0.8.217.

```bash
cd editable-project
npm ci
npm run check
npm run dev
npm run render -- --fps 60 --quality high --output Bouncy-UI-3D-Demo.mp4
```

The composition is deliberately paused when opened as raw HTML. Use the Studio preview to play or scrub, or render it with the CLI. The font and GSAP runtime are bundled to keep the appearance consistent. No image, voice or transcription service is required.

The local effect track is original synthesized audio, including soft impact tones, brief alarm accents and transition sweeps. It does not contain copied reference audio. Reference audio appears only in the clearly named reference clips and compilation.

## Practical constraints

Depth and spring amplitude should be tailored to each future video. These settings are for a standalone UI demonstration; retain clear narration timing, instructor placement and pointer alignment when adapting them to a stickman explainer. Strong 3D rotation is most useful during travel. Dense explanatory diagrams should settle faster and flatter than hero props.

The initial title begins after a short opening breath; choose an established hero frame as a thumbnail. The one-file source produces organization warnings about nested scene content. This does not affect playback, but a larger production can split scenes into sub-compositions for easier editing.
