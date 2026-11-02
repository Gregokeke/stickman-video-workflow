# Stickman Animation Sheet

Use with `Stickman Animations Workflow.md`. This is the compact motion, layout and timing sheet for the approved stickman content style. The full workflow supplies the complete production requirements.

## Frame and visual treatment

| Element | Approved starting point |
| --- | --- |
| Video | Vertical 1080 × 1920 at 30 fps. |
| Canvas | White with broad, soft dark-gray shadows extending inward near the borders. Keep the central field bright. |
| Main imagery | ImageGen-generated rounded red stick figures and relevant props with black facial and contour details; true transparent backgrounds. |
| Typical illustration container | About 860 × 1090 px, left 110 px, top 550 px. Adapt to the illustration's shape and transparent margins. |
| Caption area | Upper portion of frame, roughly left 115 px, top 220 px, width 850 px, height 260 px. |
| Caption typography | Bold condensed/slanted uppercase, approximately 60–62 px, line height about 1.12, black with selective red emphasis. |
| Caption pacing | Exact phrases from the final snapped audio; one readable phrase at a time. |

These layout values are starting points from the approved projects. Preserve faces, hands, captions and important props within readable phone-safe space rather than forcing every illustration to the same size.

## Move → stick → move

1. Design the readable resting position first.
2. Enter with a smooth visible glide, rise, scale or purposeful emergence.
3. Settle decisively and hold. Avoid bounce, elastic overshoot, perpetual hovering and arbitrary rotation.
4. When the thought develops, reposition the current subject to a supporting area or replace it with an appropriately fading handoff.

| Motion | Useful starting timing | Character |
| --- | --- | --- |
| Main entrance | 0.35–0.75 s; often 0.55–0.65 s | Controlled arrival, such as `power3.out`. |
| Reposition | Often around 0.65 s | Smooth travel, such as `power2.inOut`. |
| Ordinary outgoing fade | Start around 0.04 s after the next entrance begins; duration around 0.34 s | Reduce the old image's emphasis early while the new one arrives. |
| Caption arrival | About 0.12 s with a 12–18 px rise | Quick, clean arrival and firm hold. |
| Stroke drawing | Fit to the action and path length | Draw a bold, accurately anchored route; do not make arbitrary lines appear. |

Vary the route and staging according to the sentence. These are starting ranges, not a single transition repeated mechanically.

## Ordinary replacements versus necessary coexistence

| Handoff type | Required behavior |
| --- | --- |
| Illustration replacement | Start the outgoing fade early in the incoming movement. Do not leave both illustrations solid in the same central space. Avoid an empty gap. |
| Connected illustration and supporting prop | Retain both while they explain the same spoken thought. Make the primary focus obvious. |
| Comparison | Keep the compared subjects readable, separated and appropriately scaled. |
| Intentional emotional overlay | Preserve gradual coexistence when the overlap itself communicates the idea. |

**Project 2's ending is an intentional overlay:** the figure representing the former loving self emerges above the couch, travels upward and slowly disappears while the seated physical figure remains. Do not apply the ordinary replacement fade to this relationship.

For a minor fade correction, change the outgoing opacity timing, preserve the approved incoming motion and narration, and avoid competing transform tweens. If an existing move already controls position, fade opacity separately.

## Context and illustration density

Calculate duration from the final narration **after silence removal**. At 30–35 seconds use at least 10 distinct visuals. At 60–70 seconds use at least 22, usually planning 22–24; there is no upper cap. Use the workflow's full duration table for other lengths.

Map individual meanings and change the visual when context changes. A three-second beat is a guide; an unrelated new phrase must not inherit an earlier visual merely because its hold or animation has not finished. Do not count duplicate appearances, zooms, caption changes or file copies as new illustrations.

Each illustration needs a relevant acting state, action, object or interaction. Connected scenes may develop progressively, with one image moving aside as a related one takes focus. Keep supporting visuals only while their relationship remains meaningful.

## Sound and synchronization

Use prominent, motivated sounds: short movement swishes, solid landings, clicks for interactions, page/clock cues for passing time, and selective cracks or low punctuation for narrated emotional turns. Avoid random effects or continuous whooshes.

Place each effect on the actual movement, event or relevant word. Speech stays intelligible. No music unless requested. Keep original narration, tightened narration, separate effects and the final mix in the editable project.

## Reference use and assembly

Attach three distinct visual references when available, two minimum, to each main ImageGen request. The arms-folded, bent and pointing figure references provide useful distinct shape and gesture examples. Reference JPGs' black preview backing is not the intended canvas and contains no alpha.

Assemble with deterministic registered GSAP timelines in HyperFrames. Preserve relative paths and editable element IDs. For a small change, inspect the affected handoffs and export the matching MP4 and source ZIP. Once meaningful checks pass, deliver without unrelated extra generations or repetitive review.


## Current workspace additions — 28 October 2026
Read workflow sections 19–21 and Instructor-Guide.md for current sound-pack use and accurate, snappy, variably scaled/positioned cane presenters. The sixth reference is Sugar — Two Weeks, final nineteen-fix revision with straight-cane head tilt. Older examples remain complementary.
