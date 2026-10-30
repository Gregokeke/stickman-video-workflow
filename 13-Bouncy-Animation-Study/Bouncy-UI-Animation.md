# Bouncy UI animation — reference study and production guide

Reference: supplied `1000002059.mp4`, 576 × 1024, 30 fps, approximately 70.33 seconds. Study date: 29 October 2026.

## Purpose and evidence

This is a practical motion guide for the stickman video workflow: clocks, headline text, pills, status tags, comparison cards, badges and time-selection blocks. The supplied sleep-cycle video is the motion reference. The brief demo is an original reconstruction of its visual language, not an extraction of the reference's assets.

The entire video was reviewed in timestamped frame sequences at 0.2-second intervals. The clock selection, falling interval tags and first time-card entrance were then inspected in closer crops, including consecutive 30 fps frames for the first time card. This is rendered-frame analysis, not access to the original project. Exact easing functions, spring constants, pivot locations, source font and authored keyframes cannot be recovered from these pixels alone.

**Evidence labels:** “Observed” describes visible behavior. “Approximate” denotes a visual timing estimate. “Recipe” specifies an authored setting to recreate that behavior. Recipe values below are recommendations, not claims about the original code. Timestamps are approximate locations in the supplied file; they are not narration alignment markers.

This guide studies animation, not the accuracy of the reference's sleep advice. Time values in the demo are motion examples.

## What gives the reference its character

The UI has a fast arrival followed by a noticeably slower settling phase. It travels with direction and attitude: a pill can arrive tilted from the right, while a small subtraction tag falls and rotates into a horizontal row. Text scales up quickly from a small size. The clock has a separate alarm action, with rocking and yellow ringing strokes. Important outcomes get a color change or a small confirmation pop.

The motion resolves into readable, stationary layouts. The stacked time cards remain in place as the next one arrives. The result is cumulative explanation: the viewer remembers the previous state and watches one new step happen. The reference does not depend on every element bobbing continuously.

The perceived bounce comes from several channels working together: translation, changing orientation, size recovery and secondary accents. A generic scale-only elastic ease reproduces only one part of it.

## Full UI inventory and reference map

| Reference time | UI family | Visible behavior and role | Recreation priority |
| --- | --- | --- | --- |
| 0.0–3.8 s | Opening two-line heading | Small text rapidly expands into a heavy, centered heading; coral emphasizes the tiredness question. It holds while the character acts. | Quick text pop; keep reading baseline stable after arrival. |
| 0.0–5.3 s | Bedside alarm clock | Small coral clock, white face, dark digits; ringing marks make the alarm legible even at small size. | Separate case motion from alarm strokes. |
| About 1.5–5.3 s | Battery icon | Compact indicator above the character changes fill/state. | Bounce may introduce it; the changing fill should remain easy to follow. |
| 3.8–5.4 s | Replacement heading and question marks | New heading enters at the next thought; little question marks add a reaction beat. | Stagger the supporting symbols after the main text. |
| 5.4–14 s | Chart container and graph labels | A retained chart establishes space; LIGHT, DEEP, DREAM and a later LIGHT pill appear at relevant graph locations. White, lavender and gold classify states. | Tag pop with restrained overshoot; graph remains readable. |
| 8.2–16.5 s | Glowing chart marker | Gold point follows the drawn curve. Its glow draws attention to the active location. | Path motion is explanatory movement, not a repeated bounce. |
| 14.0–16.6 s | 90 MIN bracket and pill | A horizontal bracket denotes one cycle; a yellow duration pill arrives over it. | Reveal bracket, then pop the label. |
| 16.6–20.6 s | Secret/deep-sleep headings and chart alarm | Headlines change; a small alarm enters the chart and is positioned near a trough. A tinted chart state reinforces the warning. | Distinguish travel to a target from the ringing action after arrival. |
| 20.6–24.6 s | GROGGY / SWITCHED OFF text, battery, bulb and OFF tag | Large coral emphasis; small indicators reinforce the character's state. The OFF tag is a compact status accent. | Big text gets a short pop; small status tag gets a lighter response. |
| 24.6–28.6 s | 9 HRS / 7.5 HRS comparison panels | Two tall cards arrive in sequence; graph traces then develop inside them. Outcomes appear below. | Animate the panels as objects, then the contents as evidence. |
| About 26.8–28.6 s | Cross and check badges | Coral cross and mint check arrive at separate outcome beats. | Strong single pop with a brief recovery; no idle bouncing. |
| 28.6–33.8 s | Wake-at-cycle-end chart UI | Chart, marker, alarm and mint check communicate a better target. Text changes preserve the diagram's context. | Retain the chart; keep marker tracking separate from badge motion. |
| 33.8–36.2 s | 90-minute medallion | Gold circular badge with dark numeral and a decorative rim; prominent central arrival. It moves away as the next action takes focus. | More mass and a longer settle than a tiny tag. |
| 36.2–38.2 s | Wake-up-time clock | Coral alarm appears centrally; digits rapidly change through times, then resolve to 8:00. Case changes pose/shape subtly; ringing strokes appear near the chosen value. | Treat entry, number cycling and final alarm as distinct actions. |
| 38.2–40.6 s | Lavender −90 interval tags and leftward arrow | Tags successively fall from near the clock, rotate, and gather into a row. The clock remains above. A leftward arrow clarifies counting backward. | Directional tag travel and landing are central to the style. |
| 41.7–42.2 s | First 8:00 AM capsule | Blue pill with gold sun arrives from the right with clockwise tilt, moves left/down, then levels into its slot. | Highest-priority time-card recipe; inspect at full frame rate. |
| 43.1–48.4 s | Descending time-card stack | 6:30, 5:00, 3:30, 2:00, 12:30, 11:00 appear one at a time below retained cards. Repeated small interval marks connect the calculation. | Use a consistent card entrance with deliberate phrase spacing. |
| 49.4–53.2 s | Selected sleep-time pills and FALL ASLEEP tag | Earlier options dim; the last two change to gold and stand out. A small yellow tag appears below. | Animate selection state as well as entry. Keep chosen numerals dark on gold. |
| 53.2–56.8 s | 15 MIN stopwatch | Circular timer enters above the bed. Needle/ring movement shows elapsed allowance, and mint adds emphasis. | Pop the body once; drive progress monotonically. |
| 57.0–58.4 s | Stopwatch relocation and two time pills | Timer shrinks toward the upper right; two blue time capsules populate a new arrangement. | Move existing context instead of replacing the whole screen. |
| 58.4–60.8 s | Adjusted bedtime pills and BED tags | Times update to 10:45 and 12:15; selected pills turn gold and mint BED labels appear beside them. | Sequence value change, highlight, confirmation tag. |
| 60.8–66.3 s | Final headings and retained wave marker | A simplified sleep scene returns; headline phrases pop in above it and the gold marker continues along the curve. | Preserve reading space; reserve elasticity for the new headline. |
| 66.3–70.3 s | Platform outro | TikTok logo/loading/search UI replaces the instructional animation. | Recognized as platform outro; do not import its branding into the workflow. |

## Close reading: the time-card entrance

A 24-frame crop beginning at 41.40 s shows the first capsule outside the crop initially, then entering from the right around crop frame 10–11 (approximately 41.73–41.77 s). The sun icon leads the readable contents into view. The capsule has a downward-right tilt, travels toward a centered slot and gradually becomes horizontal. By roughly 42.1 s it is nearly level and readable. Entry-to-settle is approximately 0.4–0.5 s; the crop does not justify an exact source easing curve.

The card is one coherent object: rounded case, shadow, sun, numerals and AM suffix travel together. It does not look like four independently springing pieces. The low shadow and pill shape give it visual weight without a busy bevel. The AM suffix is smaller, but remains attached to the numeral rather than drifting during the bounce.

**Production recipe at 1080 × 1920:** arrive from x = +650 to +800 px with y = −30 to −60 px and clockwise rotation = 10–15 degrees. Travel to the slot over 0.30–0.38 s using a strong deceleration. Add a small positional/orientation recovery over 0.20–0.35 s. Finish exactly at x = 0, y = 0, rotation = 0. These are recreation settings; the extra recovery can be reduced when the reference-like slide alone already reads clearly.

## Close reading: clock and falling tags

Between approximately 36.2 and 37.8 s, the clock's displayed times change rapidly rather than counting smoothly. The chosen time resolves to 8:00 and yellow ringing curves appear. This is a selection event, not a physically meaningful passage of time. Use an explicit list of temporary values and end on the intended value. Tabular numerals prevent width changes from shaking the dial.

The lavender tags around 38.2–39.2 s begin close to the clock, tilted almost vertically. They move away and down, turning into a horizontal row. Several samples show tags at intermediate angles and heights while earlier tags already hold their positions. The reference makes accumulation visible. A uniform fade-in of a completed row would lose that explanation.

For the reconstruction, give each tag a unique final slot, a starting offset near the clock, a 70–110 degree starting rotation, and a fast downward journey. A short landing compression plus one small rebound supplies the bounce. **Compression is an authored approximation**, not a measured property of the original tags. Do not flatten the text enough to harm legibility; preferably scale a shell and keep its content on a nested child if a stronger squash is required.

## Motion presets for future projects

All durations and amplitudes here are starting recipes. Adjust them to narration timing and available space. At 30 fps one frame is about 33 ms; avoid designing a critical change that is readable for only one frame.

| Preset | Travel / starting state | Arrival | Recovery | Final hold |
| --- | --- | --- | --- | --- |
| Headline pop | Scale 0.25–0.45; y +15–30 px | 0.20–0.30 s; scale overshoot around 1.07–1.12 | 0.15–0.25 s to 1.0 | At least long enough for the complete phrase to be read. |
| Small status pill | Scale 0.4–0.65; very little translation | 0.16–0.24 s; peak 1.08–1.15 | 0.15–0.25 s | Stable until its state changes. |
| Falling interval tag | Near clock; rotated 70–110 degrees | 0.30–0.40 s fall | 0.07 s compression, 0.13 s lift, 0.20 s settle | Keep previous tags visible. |
| Tilted time capsule | x +650–800 px, y −30–60 px, rotation +10–15° | 0.30–0.38 s | 0.20–0.35 s small correction | Hold while the next row arrives. |
| Alarm selection | Clock at final location | 0.5–0.8 s temporary values | About 0.5 s rocking, decreasing angle | Stable chosen digits. |
| Confirmation badge | Scale 0.05–0.4 | 0.15–0.22 s fast expansion | 0.20–0.35 s spring settle | Stay visible with the confirmed state. |
| Selected time block | Existing card already on screen | 0.12–0.20 s color change and scale to ~1.06 | 0.25–0.35 s back to 1 | Leave other cards present but visually quieter. |
| Circular medallion | Scale 0.2–0.5, slight tilt | 0.25–0.35 s | 0.25–0.45 s controlled settle | Longer hold than a tiny tag. |
| Stopwatch | Scale/position pop on body | 0.35–0.55 s | Mild settle | Ring and hand continue smoothly; do not bounce progress backward. |

### Timing hierarchy

1. Establish the object or retained diagram.
2. Start the new motion on the relevant spoken cue.
3. Place the strongest visual emphasis on the important word or landing.
4. Allow secondary strokes, small stars or a confirmation tag to follow by about 60–140 ms.
5. Hold the result. Begin the next step while preserving enough of the previous state to explain the relationship.

A new row does not need to wait several seconds after the last row, but it must not collide with its settling motion. Use narration spacing to determine stagger; a mechanically even rhythm across unrelated phrases will feel detached from the voiceover.

### Motion anatomy and easing

For a readable spring, the first displacement is the largest. Successive corrections should shrink sharply: for example +10°, −3°, +1°, 0°. A constant-amplitude wobble looks like a loop. A long series of rebounds makes a small tag feel rubbery and delays the information.

`back.out` works well for a single intentional overshoot. `elastic.out` is useful for a small pill or badge, but its period and amplitude must be tuned. `bounce.out` describes repeated positional impacts; applying it to every property does not automatically produce the reference's motion. A deliberate multistage path is preferable for tumbling interval tags and tilted cards.

A damped spring model can be expressed as `q(t) = q_final + A * exp(-d*t) * cos(w*t + phase)`. Here A determines displacement, d controls settling and w controls oscillation rate. This is an explanatory model, not a fit to the reference. Translation, rotation and squash need not use the same amplitude or phase.

Use separate nested wrappers when different layers need different pivots: outer wrapper for travel, middle wrapper for rotation, inner shell for squash, content layer for crisp text. Never apply two simultaneous tweens to the same transform property on the same object.

## Visual construction and layout

Use a deep navy field, low-contrast star texture, heavy light headings, coral for the alarm/warning, lavender for interval tags, gold for active timing and mint for confirmation. The supplied file is compressed; its exact original palette is unknown. The demo's explicit palette is in `DESIGN.md`.

Capsules should feel wide enough for an icon, a numeral group and a small meridiem suffix. Keep the icon inset from the left edge and leave generous space around the text. Use tabular numerals. The reference's cards remain compact relative to the full portrait canvas; preserve that sense of negative space rather than stretching UI across every available pixel.

Reserve clearance for the full animated bounds, including rotation, overshoot, shadow and ringing strokes. A 590 px card rotated 13 degrees occupies a taller box than its resting 112 px height. Validate moving frames as well as the final layout. At 1080-wide export, a sensible starting row gap is 30–40 px; expand it for stronger tilt.

Do not make a tooltip touch the parent capsule's edge by accident. If a BED or interval tag sits outside the card, give it its own visible gap and enough right margin to survive phone cropping. Keep explanatory text separate from platform controls and narration captions. The demo is a UI motion test without narration captions.

## Reference-like explanatory sequences

**Counting backward:** select the wake time → finish the alarm motion → introduce one subtraction tag → land it → append a time card → retain it → append the next card. Keep all arithmetic values correct and intentional.

**Choosing an option:** complete the stack → dim irrelevant rows → highlight selected rows in gold → make the selected text dark → pop a small label. Color and contrast change together.

**Allowing extra time:** keep the existing time capsule → show the stopwatch → animate its progress → move it aside → change the displayed time → highlight the changed value → add the confirmation tag. Do not substitute a bouncing timer for an actual explanatory state change.

These patterns transfer to the stickman health videos: the instructor can point at a capsule, a gauge boundary or a timer. The UI owns its bounce; the presenter should not jitter in synchrony with every tag. Pointing must track the moving target or wait until it settles.

## Implementation pattern

The editable demo uses a single paused GSAP timeline registered as `window.__timelines.bounce`. Its timing is deterministic, so arbitrary frames can be rendered or checked. The project includes `index.html`, `DESIGN.md`, pinned dependency lock, generated local effects and build instructions.

```js
// One block, one entrance; then a shrinking correction.
function timeCard(tl, target, t) {
  tl.from(target, {
    x: 760, y: -45, rotation: 13, opacity: 0,
    duration: 0.36, ease: 'power3.out'
  }, t);
  tl.to(target, {x: -13, rotation: -2, duration: 0.11,
    ease: 'sine.out'}, t + 0.36);
  tl.to(target, {x: 4, rotation: 0.6, duration: 0.11,
    ease: 'sine.inOut'}, t + 0.47);
  tl.to(target, {x: 0, rotation: 0, duration: 0.16,
    ease: 'sine.out'}, t + 0.58);
}
```

This function uses the element's CSS position as its resting layout. Its first travel ends at that layout, followed by a small settling correction. Use wrappers if adding another independent transform. Store frame timing in seconds, not a series of browser timers. Avoid CSS infinite animations, unseeded randomness and real-time clocks in a renderable project.

## Sound guidance

The demo adds a small original synthesized effect track: soft tonal pops for entrances, a brief higher register for the alarm and a brighter accent for confirmation. It does not reuse or claim to reproduce the supplied reference's sound files. No voice service was used.

Place the principal transient at the visual contact/landing rather than blindly at the start of offscreen travel. Keep settling rebounds quieter than the initial landing. Tags can have related but slightly varied pitches; one loud identical boing on every UI item will dominate the explanation. Preserve decay tails and leave room for narration in production videos. Audio is support, not a substitute for visible mass and timing.

## Demo timeline

| Demo time | Action |
| --- | --- |
| 0.14–0.87 s | Headline and gold emphasis pop into place. |
| 0.65–1.32 s | Clock arrives with scale, position and orientation change. |
| 1.38–2.20 s | Temporary times resolve to 8:00; clock rocks and ringing curves appear then fade. |
| 2.35–3.13 s | First lavender interval tag tumbles down and lands. |
| 2.83–3.61 s | Second tag follows into a separate slot. |
| 3.80–4.54 s | Sun/8:00 AM card slides in tilted and settles. |
| 4.70–5.44 s | Moon/6:30 AM card follows. |
| 5.58–6.13 s | Mint interval badge pops beside the second card. |
| 6.12–6.61 s | Second card highlights gold, changes icon contrast and settles from a small scale accent. |
| 6.61–8.60 s | Stable reading hold. |
| 8.60–9.00 s | Gentle final fade. |

The demo compresses several reference families into nine seconds. It is not a full recreation of the original 70-second sequence, a medical explainer or a new style requirement for every future shot.

## Review checklist

- Compare the reference and demo at normal playback speed, then examine the first 15–25 frames of each main entrance.
- Does the object have a distinct direction and a clear resting slot?
- Is the first overshoot stronger than every correction after it?
- Do tags and time cards use different travel behavior?
- Do related icon, text and shell layers stay attached?
- Is the final value readable without perpetual rocking or scaling?
- Does the progress indicator move in a direction that matches the explanation?
- Are earlier steps retained when the next step depends on them?
- Do shadows, rotated corners, badges and ring strokes clear neighboring content?
- Is there a clean hold after the major reveal?
- Do sound transients align with visible events, with quiet tails preserved?
- Can a random seek reproduce the same state without waiting for real-time callbacks?
- Check encoded output, dimensions, duration, audio and full decode before delivery.

## Applying this to the established workflow

Use The Subtle Manipulator for expressive character illustration and motion. Use Reference 6 for instructor staging, pointer precision and sound cues. Use this supplied sleep-cycle reference for bouncy UI motion specifically. These are complementary roles. A polished time capsule should not replace the clean staging, correct illustration timing or necessary micro-explanation that made the approved Last Meal Tonight revision work.

The practical target is selective energy: a confident entrance, a short recovery, a useful state change and a readable hold.

## Delivered verification

The authored composition passed the full HyperFrames check with zero lint, runtime, layout, motion or audio errors; all 28 sampled contrast checks passed. One craft warning is intentional: the opening 0.14-second pause shows the background before the title enters. This is a motion test, and a later frame should be chosen as a social thumbnail. The delivered MP4 was reviewed in encoded frame sequences and checked with FFmpeg full decode. The editable package bundles the font, GSAP runtime and effect track.
