# Stickman Animations Workflow

**Production standard for original, script-led and voiceover-led stickman videos.**

Create expressive red-and-black ImageGen illustrations on a white canvas with soft inward edge shadows. Match the meaning of the narration closely, animate with fluid **move → stick → move** choreography, include precise captions, and use prominent sound effects with clear causes. Deliver a complete MP4 and a portable editable HyperFrames project.

This document is a working production specification. Read it fully before starting a video. Apply the user's current instructions to the specific project, and preserve their approved decisions during revisions.

## 1. Non-negotiable production defaults

| Area | Required default |
| --- | --- |
| Input | A supplied script, voiceover, or both. Build an original visual sequence from its meaning. |
| Format | Vertical 1080 × 1920, 30 fps. |
| Canvas | White with soft dark-gray shadows cast inward near the edges. |
| Artwork | Expressive rounded stick figures and relevant props, predominantly saturated red with black details. |
| Main visual generation | Use **ImageGen** for main characters, poses, interactions, scene illustrations and principal props. |
| Generation references | Supply **three good, distinct style references** when available; two is the minimum. Attach the actual images to each generation. |
| Transparency | Generate main artwork with a true transparent background; retain its alpha. |
| Motion | Smooth visible travel followed by a firm, readable hold. No bounce or perpetual floating. |
| Illustration changes | Start the outgoing fade early in the incoming animation; prevent competing opaque silhouettes. |
| Intentional overlaps | Preserve relationships that explain the narration, including a memory or emotional self emerging from a physically present figure. |
| Captions | Included, exact to the final recording, broken into readable phrases. |
| Voiceover | Default ElevenLabs voice: **K. V. Hagen**, voice ID **`t1yzxMpe9zK42bXmI1T2`**, for this style. Use supplied audio when available. When narration is requested, generate **one take in one generation request**. |
| Pacing | Remove silent pauses and excess dead air for tight, snappy delivery without damaging speech. |
| Sound | Prominent, purposeful movement, impact, interaction and emotional cues; narration remains intelligible. |
| Music | None unless requested. |
| Duration-based visual count | Use the narration duration **after silence removal**. **30–35 seconds: at least 10 distinct visuals. 60–70 seconds: at least 22, normally plan 22–24.** These are minimums and planning baselines, never caps. Use section 6.2 for other durations. |
| Delivery | Playable H.264/AAC MP4 plus the complete editable project ZIP, with working download links. |
| Efficiency | Reuse approved work, generate only needed artwork, make targeted corrections, and avoid repetitive review cycles. |

An illustration is a distinct generated image with a different narrative purpose or acting state. Repositioning, zooming, fading, duplicating a file, or changing a caption does **not** count as a new illustration. Do not meet the count with unused images or filler.

## 2. Workspace setup and portability

### 2.1 Bring the necessary material

For a fresh workspace, bring this file, the approved style images, the supplied transparent red-zone review canvas, any supplied narration, and the editable project if continuing an existing edit. An approved finished stickman video can serve as a craft reference for motion, caption treatment, shadow strength and sound design. It is not a source of narration for a different script.

Connect or expose these capabilities:

1. **ImageGen** for main illustrations, transparent cutouts and targeted artwork corrections.
2. **HyperFrames by HeyGen**, with access to its composition and CLI instructions, for HTML/GSAP assembly and rendering.
3. **ElevenLabs** when new narration or specifically generated sound effects are needed. A supplied voiceover requires no new speech generation.
4. Local file access, Node.js, FFmpeg/ffprobe, and a usable Chrome Headless Shell for rendering.
5. A persistent place for deliverables and editable source. Temporary working paths are not durable backups.

Do not assume another account has the same tools, permissions, voice IDs, model names, package caches, fonts, browser, files or credentials. Resolve actual capabilities before relying on them. Never invent an asset path, voice ID, generated result or download link.

### 2.2 Establish the runtime

Use Node.js 22 or newer and FFmpeg/ffprobe. Read the available HyperFrames skills and the installed CLI help. The approved project used HyperFrames **0.8.181**; that is a reproducible project baseline, not a claim about the newest release. Keep the project's package lock for repeatable installs.

Typical bootstrap commands:

```bash
node --version
ffmpeg -version
ffprobe -version
npx hyperframes init stickman-video --non-interactive
cd stickman-video
npx hyperframes info
npx hyperframes doctor
npx hyperframes telemetry disable
npx hyperframes browser ensure
```

Use the commands supported by the installed version; check `--help` when necessary. Disable telemetry with the documented CLI setting rather than guessing an environment variable. Resolve missing dependencies before starting expensive generations or a final render.

For an existing project, run `npm ci` using its package lock. Preserve its working assets and timing rather than rebuilding from scratch.

Optional local audio tooling can include Python, NumPy and a speech recognizer with word timestamps. Install those only if needed. A local recognition model may require an initial download. Use an available transcription/alignment route once instead of repeatedly reinstalling or retranscribing.

### 2.3 Keep a portable project structure

Use relative paths within the project. A practical layout is:

```text
index.html
DESIGN.md
README.md
package.json
package-lock.json
build.py
prepare_audio.py
script.txt
words.json
captions.json
storyboard.md
storyboard.json
asset-sources.json
audio-edits.json
sound-cues.json
SFX-CREDITS.md
assets/
  graphics/
  audio/
  fonts/
  vendor/
references/
renders/
```

The precise folder names may differ; the important requirement is that all referenced files are included and paths resolve after extraction. Name assets by concept and acting state, such as `unspoken-words.png`, `one-sided-effort.png`, `exhausted-at-table.png`, or `emotional-distance.png`.

Record each asset's purpose, source, generation references and local filename. Maintain reuse rights and credits for sound libraries. Save the original narration alongside the edited narration, effects track and final mix.

### 2.4 Write the visual specification before composing

Create `DESIGN.md` containing the palette, white canvas, inward edge shading, character geometry, caption style, motion ranges and overlap rules. Treat it as the project-specific source of design decisions.

Keep fonts and required libraries local when possible. Do not make a transferred project depend on temporary URLs, another account's private files, or unexplained absolute paths.

## 3. Visual identity

### 3.1 White field and inward shadows

Use a white field. Add broad, soft gray shadows extending inward from all four edges, especially the sides. The result should suggest depth just inside the frame while leaving the central illustration and captions clean and bright.

The shadow is a quiet framing treatment. Avoid a hard border, black rectangle, dirty central gray cast or a vignette that obscures hands and faces. Maintain the same shadow treatment through transitions.

One approved 1080 × 1920 implementation used a decorative overlay extending about 20 px beyond the canvas, with these CSS shadows:

```css
.edge-shadow {
  position: absolute;
  inset: -20px;
  pointer-events: none;
  box-shadow:
    inset 95px 0 120px -40px #0009,
    inset -95px 0 120px -40px #0009,
    inset 0 65px 95px -40px #0006,
    inset 0 -65px 95px -40px #0006;
}
```

Use that as a proven starting point, then judge the actual phone-size composition. Keep captions above the shadow layer if necessary to preserve their contrast.

### 3.2 Red-and-black foreground language

Approximately 90% of a typical foreground figure or prop should read as saturated red. Use black for expressions, contour separation, hands, folds, object divisions and occasional secondary detail. This is a visual tendency rather than a numerical pixel quota.

A practical starting palette is red `#ED0B10` to `#FF0000`, dark caption/contour `#101010`, white `#FFFFFF`, and neutral-gray edge shading. Select one consistent red family for the project. Caption emphasis can use a slightly darker red such as `#DE0B13` for readability.

Keep shapes confident and rounded: simple head, clear limbs, readable hands and deliberate negative space. Facial marks may be sparse, but posture must communicate the emotion. Use black separation where red hands, props or bodies meet.

Maintain a consistent figure family across the video. Keep recurring characters recognizable through proportions, facial language, hairstyle where relevant and silhouette. Follow the supplied narration's subjects and pronouns; do not automatically rewrite them.

### 3.3 Expression and gesture carry the meaning

Choose acting rather than repeatedly placing a neutral figure next to an icon. Use posture, head angle, shoulders, hands, gaze, distance and direction to make the narrated condition visible.

Examples from the approved visual language:

- Unappreciated affection: a hopeful figure offers a heart to someone looking away.
- Withheld words: a closed mouth, withdrawn face and available speech bubbles.
- Unreturned effort: a strained gesture toward an indifferent partner.
- Exhaustion: a collapsed posture with the head resting on folded arms.
- Mistaken peace: visible contentment contrasted with the other person's withdrawal.
- Lost emotional availability: fragments, a diminishing offering or a draining metaphor.
- Emotional distance: figures separated by a clear, meaningful gap.

These are examples of matching image to phrase, not a mandatory inventory for every script. Invent fresh relevant imagery for each new narration.

## 4. Style references and ImageGen requirements

### 4.1 Main artwork must be generated

Use ImageGen for the major figures, gestures, interactions, illustrations and principal props. Do not replace main artwork with code-drawn stick figures simply because the geometry appears simple.

Small SVG/CSS accents are allowed when useful: a precisely placed slash, a connecting path, a simple emphasis mark, a short bubble or a caption treatment. They must support the generated art and remain visually subordinate.

Generate one requested asset per prompt. Do not request multiple unused variants by default. When generating several independent assets, each needs a clear purpose and its own prompt. Never substitute one crowded contact sheet for individually usable scene assets.

### 4.2 Attach references to every generation

Use three distinct reference images when available, with two as the minimum. Actually attach their image files to the generation request; listing filenames in the prose is insufficient.

Assign a role to each reference:

1. Rounded proportions and red/black geometry.
2. Emotional acting, posture or hand language.
3. Line weight, contrast and expression consistency.

Choose different concepts rather than multiple copies of the same example. References guide visual grammar, while the new prompt determines the script-specific subject and staging. Do not copy a complete reference composition.

The established reference set can be stored under these relative filenames:

| Reference files | What they establish |
| --- | --- |
| `references/01-IMG-20261023-WA0029.jpg`, `references/07-IMG-20261023-WA0023.jpg` | Arms-folded figure; rounded proportions and body language. These are similar examples. |
| `references/02-IMG-20261023-WA0028.jpg`, `references/06-IMG-20261023-WA0022.jpg` | Radial light imagery and strong red shape language. These are similar examples. |
| `references/03-IMG-20261023-WA0027.jpg`, `references/05-IMG-20261023-WA0024.jpg` | Bent posture and expressive gesture. These are similar examples. |
| `references/04-IMG-20261023-WA0026.jpg` | Pointing posture and hand language. |
| `references/motion-reference.mp4`, when supplied | White canvas, motion rhythm, framing, captions and sound treatment. |

A useful three-image selection is the arms-folded figure, bent figure and pointing figure. Approved generated stickman assets can also serve as character-consistency references when appropriate.

Some reference JPGs display red art against black. That black is a preview backing, not the intended canvas and not evidence of transparency. JPG files have no alpha channel. Copy actual reference files with this guide when moving to another workspace. If they are missing, do not claim to have visually used them.

### 4.3 Prompt every asset specifically

Include the exact narrative purpose, acting, essential objects, relationship between objects, framing and exclusions. Ask for a true transparent background explicitly.

Reusable prompt structure:

```text
Use case: illustration-story.
Asset: [specific concept and acting state].
Purpose: illustrate the spoken phrase “[exact phrase].”
Reference roles: image 1 proportions; image 2 acting; image 3 line weight.
Style: expressive rounded stick figures, predominantly solid saturated red,
with sparse black expression and contour details; clean flat graphic artwork.
Subject/action: [precise posture, gaze, hands and object interaction].
Composition: [number of figures, relative positions, full body or close-up].
Background: truly transparent; retain alpha.
Constraints: coherent hands, readable silhouettes, complete required props,
generous clear margins, no baked captions, no lettering, no scenery or backing.
Avoid: realistic rendering, dimensional material shading, gradients,
white outlines, crowded unrelated symbols and duplicate generic gestures.
```

Use additional constraints only when they help the actual asset. Be explicit about whether a prop is standalone or part of a coherent interaction.

### 4.4 Separate moving parts intelligently

An interaction can be one combined illustration when its internal acting must stay coherent: a kneeling figure reaching toward another person, for example. If a heart, phone, bag, page or other object must move independently, generate it separately or plan a separate usable layer.

Do not animate a whole combined image as if one embedded hand or prop were an independent object. Use the asset's actual geometry and available layers. Keep every independently animated element addressable in the project.

Inspect the necessary properties once: transparent background, correct red/black treatment, meaningful expression, complete hands and limbs, required objects, clean silhouette and no unwanted text. Review on the final white field; a dark image viewer can conceal black details. Request a targeted correction only when a material problem prevents use.

## 5. Narration intake and tight audio preparation

### 5.1 Establish the authoritative recording

Read or listen to the complete supplied recording. Extract its actual wording and meaning. Do not assume its script matches an earlier message, reference clip or previous project.

If script and recording are both supplied, compare them. Use the approved recorded wording for captions and timing. Resolve a meaningful mismatch before creating visuals that depend on the disputed wording.

Keep the original file untouched. Save an edited copy and an audio-edit map. Never substitute narration from a style reference because a generation failed unless the user explicitly authorizes that substitution and the wording is appropriate.

### 5.2 One take when new narration is needed

The default ElevenLabs voice for this stickman video style is **K. V. Hagen**, with **voice ID `t1yzxMpe9zK42bXmI1T2`**. Use this exact ID for new narration unless the user explicitly requests a different voice. This is the user's designated voice for the style; do not choose a substitute merely by matching a voice name or description. Confirm access to this ID in a fresh account or workspace. If it is unavailable, report the issue before substituting a voice.

Use the supplied recording when one is provided; the default voice ID does not authorize regenerating or replacing approved audio.

Use the user's requested **ElevenLabs v4** when available. Confirm the actual model identifier supported by the connected tool. Do not silently substitute another voice or model. Generate one take in one request. Do not trigger extra takes to obtain timing, change visuals, repair a render or test minor wording.

If the requested generation is rate limited or fails, explain the actual condition and obtain direction before making another submission or substituting audio. Uploaded narration should be processed directly.

### 5.3 Remove silence for snappy delivery

The default is tight narration with silent pauses and excess dead air removed. Preserve spoken words, consonants, natural articulation and vocal character. Tightening should not sound chopped or accelerate the speaker artificially.

A proven local starting point is FFmpeg silence detection around `-36 dB` with a minimum interval around `0.16 seconds`. In the approved edit, detected gaps longer than approximately `0.18 seconds` were shortened while retaining about `0.035 seconds` at each side. These values are starting points for the recording, not universal thresholds.

Typical detection command:

```bash
ffmpeg -hide_banner -i source.mp3 \
  -af silencedetect=noise=-36dB:d=0.16 -f null -
```

Save the detected intervals and the intervals actually removed. Adjust boundaries when quiet speech or a breath is mistaken for silence. Use very short fades at edit boundaries if needed to prevent clicks; do not crossfade away syllables. Preserve a pause that is essential to meaning or explicitly requested, while keeping the overall delivery tight.

One approved recording was reduced from about **79.39 seconds to 68.78 seconds**, producing a **69-second** final video with a short tail. Another was tightened from about **42 seconds to 36.7 seconds**. These are examples of actual edits, not duration targets for a new script.

### 5.4 Obtain timestamps after editing

The edited recording becomes the definitive clock. **Determine the required visual count only after snapping the audio and removing silence.** Measure the actual tightened narration; do not use the original file duration, an estimated reading time or a padded video outro. Save this measured duration with the selected minimum count. Obtain word timestamps once from that version, or accurately transform existing alignment through the saved edit map. Do not align to the original and then remove gaps without retiming everything.

Save words with start/end times, exact transcript text, phrase-level caption groups, duration and silence edits. Correct obvious token splits such as `check` + `-ins` while preserving the actual wording. Avoid unnecessary paid transcription when a usable transcript and alignment already exist.

If audio changes later, retime captions, visual cues and sound effects together. A visual-only correction should preserve the approved recording and its timing.

## 6. Detailed phrase-to-visual planning

### 6.1 Map the script before generating

Identify the argument, emotional progression, important nouns, verbs, metaphors, comparisons, reversals and closing instruction. Every relevant idea must have a deliberate visual response.

Use roughly **three-second visual beats**, flexing to **3–5 seconds** when an idea needs a readable hold. A word that changes the meaning should trigger a visual response on that word, even within a longer beat. A response can be a new illustration, a connected prop entering, a meaningful gesture/state change or a carefully chosen reframing.

Do not leave a generic illustration unchanged over several distinct claims. Do not cut away so quickly that the viewer cannot understand a relevant interaction.

### 6.2 Determine a minimum from the tightened audio, then build the inventory

**First snap the audio, then measure it, then determine the visual minimum.** Let `T` be the exact duration in seconds of the final narration after silence removal. A decorative intro, end card, quiet tail or rounding the display duration must not change the selected count band. If the narration is edited again, recalculate the minimum before locking the inventory.

The two explicitly established duration bands are:

| Tightened narration duration | Required minimum distinct visuals | Planning baseline | Upper limit |
| --- | --- | --- | --- |
| 30–35 seconds, including both endpoints | **10** | Start with 10 or more, then add what the exact contexts require. | **None.** |
| 60–70 seconds, including both endpoints | **22** | Normally plan **22–24**, then add more whenever the script needs them. | **None; 24 is not a cap.** |

**Exactly 70 seconds still requires at least 22 visuals.** The final 22–24 baseline governs the entire 60–70-second band. The approved 69-second edit used 22 distinct illustrations across 27 planned visual beats.

For durations outside those two established bands, use these derived planning defaults to keep the scaling predictable. These interpolate between the established bands and extend the same density beyond them; they do not introduce a ceiling. A later explicit user requirement takes precedence.

| Tightened narration duration `T` | Minimum-count calculation |
| --- | --- |
| Above 0 and below 30 seconds | `max(1, ceil(T / 3))` |
| 30 through 35 seconds | `10` |
| Above 35 and below 60 seconds | `ceil(10 + 12 × (T − 35) / 25)` |
| 60 through 70 seconds | `22` |
| Above 70 seconds | `22 + ceil((T − 70) / 3)` |

`ceil` means round upward to the next whole number. Examples of these derived defaults: 45 seconds → at least 15; 50 seconds → at least 18; 75 seconds → at least 24; 90 seconds → at least 29. Use the exact measured duration in the calculation rather than rounding it into a lower band.

The minimum is a **floor**, not a target that overrides meaning. Plan at least that many relevant distinct visuals, then increase the count whenever the narration introduces additional subjects, actions, conditions, comparisons, consequences or reversals. A 65-second script that needs 27 visuals should receive 27; do not stretch 22 images or compress different contexts together to stay within 22–24.

Count only distinct final generated illustrations or principal standalone props that are actually used in a meaningful context. Give each an asset ID and a precise narrative purpose. A generated coherent interaction can count as one illustration; its embedded figures do not each become a separate illustration. Zooms, pans, fades, repositioning, repeated appearances, copied files, caption changes and minor code-drawn accents do not increase the distinct visual count. Do not count discarded or unused artwork.

If the first inventory is below the minimum, revisit the script for separate acting states, objects, actions, contrasts and consequences that deserve their own artwork. Build out that relevant detail. Do not meet the number with unrelated props, redundant near-identical poses or rapid filler flashes. Each counted visual must have enough readable screen time to communicate its assigned meaning.

Record `tightened_audio_duration`, `minimum_visual_count`, `planned_distinct_visual_count` and `used_distinct_visual_count` in the production notes. The final used count must meet the minimum; the context audit in section 6.3 must also pass. Neither a sufficient count nor attractive animation excuses an incorrect visual match.

### 6.3 Make context matching precise

- Show the action, not only a related noun. “He stops asking” needs visible withdrawal or unreturned effort, not an arbitrary heart icon.
- Distinguish cause, consequence, mistaken interpretation and proposed response.
- Respect negation. If a line rejects an interpretation, make that rejection clear through captions, staging or a purposeful mark.
- Introduce a metaphor when it is spoken. Do not show the consequence before the setup unless the script deliberately previews it.
- Keep supporting objects specific to the current idea. Do not fill space with unrelated symbols.
- Match the exact pronoun, emotional state and relationship in the recording.
- Reuse an illustration only while its actual pose and meaning remain appropriate.

**Audit context at the phrase level, not only at scene boundaries.** Mark the start and end of every individual idea and assign its exact illustration or visual development. A three-second beat is a pacing guide, not permission to keep an image through an unrelated phrase. If the context changes after one second, respond at that change rather than waiting for a fixed interval.

For each visual, record the phrase it represents, the relevant subject/action/emotion, its first useful appearance and the last phrase it can truthfully support. Replace or develop it when that meaning changes. Do not leave a visual from context A as the main illustration for different context B because it is convenient, because its animation is still running or because the minimum count has already been reached.

Distinguish closely related but different meanings: unreturned effort, begging, exhaustion, silence, apparent peace and actual emotional withdrawal need precise treatment rather than one generic sad figure stretched across all of them. Do not repeat the same illustration across separate contexts merely because both concern a relationship or share a broad emotion.

An earlier visual may remain as a supporting element only when it still explains the current idea. State that relationship in the worksheet. During an ordinary replacement, its brief outgoing fade is a transition, not an excuse for a prolonged context mismatch. Preserve intentional overlays and connected demonstrations when their coexistence directly serves the narration.

### 6.4 Choose between focused and connected scenes

**Focused scene:** one illustration receives attention because the narration is developing one idea. A close-up or measured reposition may reveal its relevant detail.

**Connected scene:** an established subject moves to a supporting position while a second illustration or prop enters. Keep both when their relationship explains the phrase: a relaxed person beside a calendar, for example, when the narration mentions weeks without an argument.

**Illustration replacement:** the earlier image has finished its job and the next image takes over. Use an early outgoing fade rather than leaving both opaque.

**Intentional overlay:** two images coexist because their overlap itself carries meaning. A former loving self rising and fading above a physically present seated figure is a purposeful emotional overlay. Preserve that relationship instead of applying a blanket cleanup rule.

Vary scales and arrangements according to the script: full figure, two-person exchange, object close-up, simple relationship illustration, prop demonstration and a selective typography-led beat. Keep the frame arranged and readable.

### 6.5 Complete the production worksheet

| Final audio time / exact phrase | Meaning and emotion | Illustration / separate parts | First held layout | Move → stick → handoff | Caption / sound | Source / references |
| --- | --- | --- | --- | --- | --- | --- |
| Word-aligned interval | What the viewer should understand | Specific figure, acting state and relevant objects | Position, scale and layering | Entry, hold, next change and overlap type | Exact phrase and motivated cue | Existing approved asset or new generation with attached references |

For each handoff, label the overlap **replace**, **retain together**, or **intentional overlay**. This prevents the fade correction from removing an important relationship.

Derive the asset list and sound plan from the worksheet. Generate only the pieces needed by it. Update the worksheet when the final edit changes.

## 7. Composition and phone-size readability

Build the fully readable resting frame before adding animation. Place the subject where it will be when settled, and then design its journey into that position.

Keep faces, hands, important props and captions within safe viewing areas, with enough margin for the inward shadows and platform interface. Deliberate off-screen travel is allowed during movement; important body parts should not remain accidentally clipped in a held frame.

In the approved 1080 × 1920 layout, captions occupied an upper area around 220–480 px from the top, with illustrations generally staged below. An artwork container around 860 × 1090 px starting near 550 px from the top was a useful baseline. Adapt to the image's actual transparent margins and aspect ratio rather than forcing every asset to identical apparent size.

Use negative space to separate interacting bodies and props. Do not cover expressions with captions. A two-image scene should have an obvious primary focus. Avoid red-on-red tangles, accidental scale changes between comparison figures, and visible bounding boxes or matte backgrounds.

Keep a strong first-second action. A hook can establish a readable interaction immediately, then develop it with a connected visual rather than waiting through a static opening.

### 7.1 Mandatory review with the supplied red-zone canvas

Use the actual user-supplied transparent red-zone PNG as a required review overlay for every finished video from this point onward. Transfer it with this workflow and each editable project as `references/red-zone-canvas.png`. It marks the video areas covered by the platform interface; the right-hand action rail needs particular care. This specific canvas is authoritative for the check. Do not substitute remembered generic platform margins or add phone bezels and operating-system navigation that are not in the supplied canvas.

Scale the complete guide to the exact video canvas, keeping its frame aligned. Review the whole timeline, including readable holds, paired/triple layouts, entrances, outward movements, comparisons, captions, callouts and the ending. Check the visible pixels of the actual illustration rather than treating transparent image padding as content. Spot-check the exported MP4 with the guide as well as the composition. Keep the guide as a review layer; the delivered video must not contain the red UI overlay.

Ordinary props, faces, hands, important illustration details, phone text, captions and explanatory lines must stay out of the marked red areas and must not sit behind them. Pay special attention to right-hand supporting props and large two-image comparisons. If a normal object intrudes, move it inward, revise its paired spacing, proportionally reduce it where needed, or adjust its travel route. Preserve aspect ratio, context, animation rhythm, caption placement and approved sound/narration timing. Do not hide an error by simply masking off important content beneath the UI.

**Narrow exception:** a genuinely very large illustration may deliberately extend partly off-screen as an intentional part of the composition. Preserve that case when the deliberate staging is clear and its important information remains readable. Record the exact asset and time range when relying on this exception. A user-specified large layout, such as a huge ten-step routine extending down/left behind a centred SCAM stamp, is an intentional exception to preserve. Being placed on the right, entering/exiting, or belonging to a crowded group does not by itself qualify. Do not use a blanket large-object exception for ordinary props.

Review at phone size with the actual guide visible. For dense motion, use frequent timeline samples and alpha-aware overlap checks, then inspect flagged handoffs visually. Faint decorative shadows are not the same as hidden foreground information; keep the actual subjects and text clear. Move attached paths and scan effects with their subjects, or recalculate their anchors and remove them before the subjects move away. Recheck affected scenes after a placement correction. Record the guide used, corrections made and any deliberate large-object exceptions in the project notes. Once the relevant checks pass, export and deliver the clean video with its matching editable project.

## 8. Fluid move → stick → move animation

### 8.1 Entrance and hold

Make entrances visible and smooth: controlled glide, rise, scale, curved travel or a meaningful emergence from behind another object. Finish decisively at the designed resting position.

Use entrance durations around **0.35–0.75 seconds** as a starting range. The approved edit often used roughly **0.55–0.65 seconds**. Use easing such as `power3.out` for a clean arrival and `power2.inOut` for a reposition. Vary motion direction and staging without introducing bounce.

After arrival, hold the image still enough to read. Avoid elastic overshoot, rubbery settling, continuous bobbing, aimless rotation or decorative hovering. Smoothness comes from controlled acceleration and choreography, not constant motion.

### 8.2 Repositioning develops a thought

An image can move from center to a side, reduce in scale or recede into a supporting role while another enters. Its destination must leave space for the incoming subject. Choose travel direction from the relationship between the graphics and the spoken thought.

Do not recycle the exact same transition across every scene. Vary scale, route and composition while keeping the motion language consistent. Do not use an instantaneous jump where visible travel is needed.

### 8.3 Ordinary changes need an early outgoing fade

**The outgoing illustration must lose opacity during its outward movement, early enough that it does not remain a competing solid silhouette under the incoming image.** Do not wait until the incoming illustration has nearly settled before beginning the fade.

Use the incoming entrance as the timing anchor. A proven refinement started ordinary outgoing fades about **0.04 seconds after the incoming entrance began**, with a fade around **0.34 seconds** and a quick, smooth opacity ease. The incoming travel generally lasted about 0.6 seconds.

For example, if the new image starts entering at 10.00 seconds, begin reducing the outgoing image around 10.04 seconds. It should be substantially subdued while the new image takes focus, with a continuous handoff and no blank screen. Use the actual movement and shapes to tune this; do not apply the numbers blindly to every relationship.

Practical rules:

1. Begin outward movement or repositioning as the thought changes.
2. Begin the outgoing fade early in the new entrance.
3. Keep the new image arriving while the old image loses emphasis.
4. Avoid two equally opaque illustrations crossing through the same central space.
5. Avoid an empty gap created by completing the old exit before the new entry begins.
6. Judge the transition during the overlap, not only the settled frames.
7. If outward movement already controls `x`, `y` or `scale`, fade opacity separately rather than starting a conflicting tween on the same transform property.

The intended result is a clean, fluid visual replacement. Brief overlap is useful; a late, solid double image is not.

### 8.4 Preserve meaningful overlaps

Do not globally fade every earlier element as soon as a new one appears. Retain images that explain one another. Keep foreground/background layering deliberate and make the viewer's focus clear.

The approved ending is a specific example: the seated figure and couch remain physically present while the image representing his former loving self emerges above them, travels upward and slowly disappears. The gradual coexistence is the meaning of the scene. Preserve that slower overlay when refining ordinary transitions.

When revising fades, identify these exceptions before editing. Do not shorten an intentional emotional overlay, erase a useful comparison or detach a relevant supporting prop.

### 8.5 Paths, circles and accents

Use a line only when it traces a real route, connection, contour or negation. Anchor its endpoints and route to the appropriate objects. Make it bold enough to read on a phone and animate its drawing visibly along the intended path.

If the object moves, the path must move with it or update coherently. A slash must cross the intended item rather than float above it. A circle must fit the actual feature being emphasized. Avoid arbitrary arcs and decorative lines with no explanatory purpose.

## 9. Captions and selective editorial type

Captions are part of the default finished video. Generate them from the final tightened audio and preserve the exact spoken wording. Keep caption text separate from generated artwork for sharp rendering and easy correction.

Use bold, condensed, italic or slightly slanted uppercase type, primarily black with selective red emphasis. The approved layout used approximately 60–62 px type at 1080 × 1920, with a generous centered width around 850 px and line height around 1.12. Match apparent size and weight, then adjust for the actual font and phrase.

Break by meaning rather than arbitrary word count. Usually use 3–6 words, flexing for a complete short phrase. Prefer “a funeral for his feelings” followed by “in his head” over leaving an isolated preposition at the end of a caption. Keep a short final statement together when readable.

Use one phrase at a time, with a quick smooth arrival and a firm hold. A subtle rise around 12–18 px over roughly 0.12 seconds is sufficient. Remove the previous phrase on time so captions do not double up. Highlight a few meaningful words, not every other word.

Avoid covering expressions, tiny text, forced line breaks that cause unexpected wrapping, or long blocks of transcript. Check safe width and line count at phone size. Additional in-scene words should clarify a metaphor or reversal rather than unnecessarily repeat the captions.

## 10. Prominent, purposeful sound design

Sound effects must be audible and solid, with a reason to occur. Match their onset to the visible action or exact narrated turn.

| Action or meaning | Suitable sound treatment |
| --- | --- |
| A deliberate entrance or slide | Short controlled swish or brush. |
| A substantial object settling | Brief low impact with an audible transient. |
| A pointed interaction or mute action | Crisp click or tick. |
| A message or disappearing check-in | A restrained notification/click that stops with the action. |
| Passing pages or weeks | Page movement or a few paced ticks. |
| A break, tear or emotional fracture | Short crack, tear or restrained glitch. |
| A draining or diminishing sequence | Descending or weakening cues aligned to its steps. |
| A genuine emotional reveal | Selective low punctuation or a brief tonal cue. |
| A quiet, important line | Space for the narration to carry it. |

Do not scatter random impacts, play a whoosh over every word, or rely entirely on sub-bass that disappears on phone speakers. Use transient detail and frequency balance so effects remain audible at ordinary listening levels.

Reuse approved licensed effects where they fit; generate only missing specific sounds. Keep credits and source information. A longer detailed edit may contain many cues—the approved 69-second edit used 40—but that is a record of that edit, not a quota. Each cue must earn its place.

Mix once against the final narration. Keep speech clearly dominant, preserve consonants and avoid sharp volume jumps. Control effect peaks and the combined mix so it does not clip. Keep a separate effects track for later adjustments and include the final mix in the project. Do not add background music unless asked.

## 11. HyperFrames assembly requirements

Use HTML/CSS for layout and registered deterministic GSAP timelines for animation. The editable composition is the source of truth.

- Set the root composition's width, height, start and final duration explicitly.
- Use a paused timeline registered in `window.__timelines` under the correct composition ID.
- Build the timeline synchronously so the renderer can discover it.
- Keep stable IDs for illustrations, captions, overlays and props.
- Use relative media paths and local copies of required assets.
- Keep audio in the framework's supported audio elements and tracks.
- Avoid random or wall-clock-driven movement and infinite animation repeats.
- Avoid concurrent tweens fighting over the same property on the same element.
- Make caption exits deterministic so only one phrase remains visible.
- Preserve all required timing metadata supported by the installed framework.

Follow the installed framework's actual playback and capture rules while implementing the user's choreography. Keep scene handoffs continuous, with an entering visual and the correctly fading or retained outgoing visual.

Typical project commands, subject to installed-version support:

```bash
npx hyperframes lint
npx hyperframes validate
npx hyperframes inspect
npx hyperframes snapshot --at 1.5,7.0,19.2 --output review-frames
npx hyperframes preview
npx hyperframes render --fps 30 --quality high \
  --output renders/final.mp4
```

Some versions consolidate validation and inspection into `hyperframes check`; use the equivalent supported commands rather than repeatedly invoking deprecated ones. A two-worker render worked for the approved project; select workers according to actual memory and browser stability. Do not increase concurrency merely to use available cores.

If rendering fails, diagnose the existing project and dependency/runtime issue. Do not regenerate narration or artwork to repair an export problem.

## 12. Efficient review and export

Review deliberately, once per meaningful change. Focus on the hook, dense scenes, meaningful phrase-to-visual cues, shared-space transitions and the ending. A small contact sheet and a few transition samples are more useful than repeated broad checks with no new concern.

Before rendering, resolve missing assets, broken paths, clipped text, obviously incorrect layering and animation-property conflicts. Check the actual overlap intervals to confirm early fades. Confirm that intentional overlays remain intact.

Render after the relevant issues are resolved. Avoid repeatedly changing approved scenes during the export phase. Report progress honestly: a queued export, active render and completed file are different states.

Deliver an MP4 with **H.264 video, AAC audio, 1080 × 1920, 30 fps**, using broadly compatible pixel formatting such as `yuv420p`. Ensure the container is complete. Never deliver a partial render merely because its filename ends in `.mp4`.

Use FFprobe and one full decode to detect incomplete or unsupported files:

```bash
ffprobe -v error \
  -show_entries format=duration,size:stream=codec_name,pix_fmt,width,height \
  -of json renders/final.mp4

ffmpeg -v error -i renders/final.mp4 -f null -
```

Check the finished output's opening, major transitions, end and audio as needed. Do not claim that a phone playback test occurred unless it actually did. Once the appropriate checks pass, deliver; do not add repetitive review steps without a new issue.

## 13. Minor revisions and preservation of approved work

For a requested correction, identify exactly which properties, assets or time ranges need changing. Preserve all other approved decisions.

For a fade correction:

1. Identify ordinary replacements and intentional coexistence separately.
2. Advance outgoing opacity reduction on ordinary replacements.
3. Keep existing entrances, caption timing, sound cues, narration and artwork unless the correction specifically requires otherwise.
4. Avoid transform conflicts introduced by moving a fade earlier.
5. Preserve the intentional final emotional overlay and any connected prop relationships.
6. Review a few affected handoffs, render the corrected file and update the editable project.

Use existing assets for animation-only changes. Do not generate fresh images or another voice take for a minor timing adjustment. Keep a reversible checkpoint privately, but package the final source rather than confusing the user with discarded versions.

## 14. Editable project and final delivery

The project ZIP must open in another capable workspace without needing files from this session's temporary directories.

Include:

- `index.html` and any sub-compositions.
- `DESIGN.md` and clear reproduction instructions in `README.md`.
- Package manifest and lockfile.
- All used generated illustrations and independently animated props.
- Required fonts and locally used animation libraries.
- Original supplied narration, tightened narration, effects track and final audio mix.
- Exact script, word timestamps, caption groups and audio-edit map.
- Phrase-by-phrase storyboard and sound cue map.
- Asset sources, supplied style references and sound credits.
- Any build scripts required to reproduce or revise the edit.

Do not bundle `node_modules`, caches, temporary render work directories, discarded generations or review screenshots by default. The rendered MP4 can be delivered alongside the editable ZIP; it need not inflate the source package.

Save the final MP4 and ZIP durably before delivery. Provide actual working file links with clear filenames. Never use an invented path or an internal API URL as a substitute for a usable attachment. If a file is incomplete or cannot be made available, say so plainly and finish the necessary repair.

Deliver one finished video by default, together with its matching editable project. Do not provide alternate takes or multiple stylistic versions unless requested. For a revision, update both deliverables so their source and rendered result agree.

## 15. Production checklist

### Before generation

- Read this workflow and the supplied script/recording.
- Establish the exact narrated wording, subjects, emotional progression and ending.
- Tighten audio, measure its exact duration after silence removal, and establish its definitive timing.
- Calculate and record the duration-based minimum from section 6.2 before locking the inventory.
- Complete the phrase-level worksheet, including each visual's intended context and last relevant phrase.
- Plan at least 10 distinct visuals for 30–35 seconds, and at least 22 for 60–70 seconds, normally starting with 22–24 in that longer band. Apply the documented scaling rules to other durations.
- Treat the counts as minimums with no cap; add any additional illustrations required for precise context matching.
- Select and attach two or three distinct references for each generation.

### Before rendering

- Main artwork is ImageGen-produced and truly transparent.
- Visuals match the relevant words, actions, comparisons and negations.
- The final used distinct visual count meets the minimum for the tightened narration duration.
- No illustration is stretched into a different context, repeated as a substitute for new meaning, or held longer than its assigned idea remains relevant.
- Characters, expressions, hands and important props read at phone size.
- White canvas and inward shadows remain consistent.
- Captions use the exact recording and readable phrase breaks.
- Entrances are fluid; resting frames hold firmly.
- Ordinary outgoing images fade early; no late solid double silhouettes.
- Useful side-by-side relationships and intentional emotional overlays remain.
- Lines and emphasis marks are bold, meaningful and accurately attached.
- Sound cues are prominent, motivated and aligned; speech remains clear.
- No missing files, accidental clipping or conflicting animation properties remain.

### Before delivery

- Review the full edit and representative exported MP4 frames against the actual red-zone canvas, especially the right-hand controls; correct ordinary intrusions and document any genuinely large intentional off-screen illustration. Keep the guide out of the delivered video.
- The render is complete, playable and correctly encoded.
- The project contains all source needed for transfer and future edits.
- The MP4 and editable ZIP reflect the same final revision.
- The files are saved and their download links are usable.
- No unnecessary extra generation, variant or review loop delays delivery.

## 16. Creative standard

Every illustration must answer the words currently being spoken. Every movement must establish, develop or hand over that meaning. Every sound must have a cause. Let an image arrive fluidly, hold clearly, and give way cleanly when its role is finished. Keep meaningful relationships visible, preserve intentional emotional overlays, and make each new script visually specific within this consistent stickman language.


## 17. Added craft standards — character prominence, original motion and illustration depth

These additions preserve all earlier sections. Apply the latest explicit project direction where an older example differs. Visual counts remain minimums, never caps; select as many exact context illustrations as the recording requires.

### 17.1 Character size is judged by visible artwork, not its transparent container

Review the actual head, expression, hands and body at phone viewing size. A large PNG or CSS wrapper can contain a small visible character because of transparent padding. Measure or inspect the nontransparent silhouette before deciding that an asset is large enough. In a multi-person illustration, inspect each individual person; total group width does not guarantee readable faces.

Keep the main character prominent and immersive. Avoid two equally tiny graphics floating in a mostly empty frame. In a pair, establish a clear hero and a relevant supporting subject. The supporting character may be smaller, but its expression, gesture and interaction must still be readable without zooming or straining. Ingredient icons can be smaller when their recognizable shape communicates the exact phrase; this is not permission to miniaturize people.

A useful starting composition is a larger central or slightly offset hero with a moderately smaller subject down to the left or right. The side subject need not sit on the same baseline as the hero. Use diagonal or staggered heights to preserve readable scale while clearing the right action rail. A lower subject must remain mostly visible, outside the normal bottom interface zone and separated from captions. Keep the approved caption position fixed. Do not push every scene to the bottom or center every item mechanically.

When safe-area checks reveal crowding, first revise spacing, vertical staggering, hierarchy and the route of travel. Uniformly shrinking everything until it fits can technically clear the guide while producing an unusably tiny scene. Fit and readability must pass together. Retain aspect ratios. Use the actual red-zone guide, not a guessed universal rectangle. Intentional oversized offscreen artwork remains a narrow, documented exception under section 7.1.

At 1080 × 1920, the revised final reset character in Gut to Glass uses about 618 px of visible height; the supporting two-person illustration uses about 440 px of group height. These are project-specific demonstrations of hierarchy, not universal scale multipliers or hard minimums. Portrait cards, tall phones and wide groups have different source padding and proportions. Review the result at phone size.

### 17.2 Preserve the original connected animation language

Study the editable sources of Protect Their Peace and When He Goes Quiet, including the clean-fades revision. Their choreography is a continuing part of this style, not an optional historical reference. The original project study is recorded in OG-MOTION-STUDY.md in the current source package.

- **Large lateral arrival:** an incoming character glides across a substantial distance and settles at a readable hero scale. Do not substitute the same small upward pop for every subject.
- **Center to side with a retained subject:** the established subject travels diagonally or laterally, reduces moderately and holds as a relevant supporting character while the next hero enters. Project 1 around 4.50–5.30 s moves the loving figure left and down at scale 0.59 while the schemer arrives from the right. The technique depends on the original asset's visible silhouette; copying 0.59 blindly into another padded PNG is incorrect.
- **Return to hero:** a retained subject moves back toward the center and regains prominence when the narration returns to it. Project 1 around 8.30–9.00 s demonstrates this. Preserve connected continuity instead of repeatedly deleting and reintroducing the same relevant subject.
- **Selective depth emergence:** a new relevant detail can emerge from behind or near the established subject, enlarge and settle in its own clear space. Project 1 around 11.05–11.75 s uses a rising foreground arrival. Keep meaningful associations clear; avoid arbitrary overlap.
- **Focused push-in:** a settled hero can enlarge once during a meaningful word or revelation, lift slightly and hold. Project 1 around 22.50–23.15 s demonstrates a deliberate scale 1.23 emphasis. This is a finite motion, not continuous breathing or floating.
- **Travelling early fade:** ordinary replacements continue their outward travel while becoming transparent early enough to prevent distorted overlap. Project 2 around 6.65–7.46 s and 23.45–24.22 s demonstrates the handoff. In the current edit, an outgoing opacity fade often starts about 0.04 s into travel and lasts about 0.30 s. Judge the actual shared frames and do not turn these starting values into a rule that clips useful meaning.
- **Finite prop interaction:** a relevant prop joins a retained character, then performs one or two motivated movements keyed to sound. Project 2 around 31.98–33.80 s uses calendar ticks. No perpetual idle wobble.
- **Meaningful layered exit:** Project 2 around 65.50–67.68 s lets the former emotional self rise and fade behind the seated physical body. Preserve this deliberate narrative overlap. Do not confuse it with an ordinary illustration replacement, and do not insert an unrelated ghost effect into a health script.

Use smooth move → stick → move rhythm. Firm holds allow the audience to read the illustration. Motion variety comes from different spatial relationships, travel directions, hierarchy changes and narrative causes, not random presets or constant movement. Maintain clear dominant subjects during the entire move, including the supporting hold.

### 17.3 Faint directional shadows behind the illustrations

The soft inward canvas edge shadows and the individual illustration shadows are separate treatments. Keep both. Every major red-and-black cutout should have a faint, dark, softly blurred directional shadow behind its actual silhouette. It should create separation from white without looking like a thick gray duplicate, solid outline, muddy halo or extra prop.

A proven 1080 × 1920 starting point in Gut to Glass is:

```css
.asset img {
  filter: drop-shadow(-13px 18px 12px rgba(0, 0, 0, .30));
}
.asset.photo img {
  filter: drop-shadow(-10px 16px 12px rgba(0, 0, 0, .22));
}
```

Use true transparent assets. Apply the shadow to the image silhouette, rather than casting a rectangular shadow from a transparent wrapper. Do not double an already baked-in heavy shadow. Judge strength at the final rendered scale: scaling the illustrated wrapper also changes the apparent shadow. Maintain consistent light direction through scenes. Keep shadows subtle around portrait cards, fine details, drawn paths and phone text. Review foreground ink separately from faint decorative shadow when checking the red-zone guide.

### 17.4 Stamp scene separation and held-frame clarity

For the revised “officially a scam” scene, the SCAM stamp stays centered and imposing. The ten-step routine illustration is lower at bottom left and moderately reduced from its earlier oversized version. Keep a deliberate visible white gap between the stamp and the routine, including its character, receipt and bottles. Do not let stamp edges touch the character or make tangencies that confuse the silhouette. The routine remains readable and can deliberately extend below the frame under the documented oversized-art exception. Its exception does not permit the stamp to hide behind platform controls.

Check the most visible held frame and intermediate frames, not only the endpoint transform. Confirm that incoming movement, shadows and early outgoing fades do not destroy the gap. Do not fix an unwanted overlap by shrinking both subjects into tiny icons.

### 17.5 Preserve the later approved refinements

Keep narration tight without cutting expression endings. Use genuine detected silence, not transcript-estimated interword gaps. The later approved gentle pass used detection around −42 dB, cut only real gaps longer than about 0.26 s, and retained about 70 ms at each boundary. These are starting values: listen to every join and retain longer breath or consonant tails when needed. Do not repeat the rejected aggressive word-gap pass that clipped speech around “Newsflash.” Never stretch the supplied narration merely to hit a visual count.

Keep matching phone frames uncluttered: one clear action per screen, readable headings and no repeated Remea branding across every mockup. Where a scan screen already carries the brand, following analysis, results and plan screens need not repeat it. Use prominent, motivated sound effects that remain clear without masking narration; preserve approved timing during layout-only revisions.

Every explanatory line, slash, arrow or circle must draw progressively along its actual path, be thick enough to read, connect precise targets and serve the spoken meaning. Attach it to the moving subject or update its coordinates, and clear it before an unrelated transition. Preserve the higher illustration placements, fixed upper captions, photographic same-person comparison cards where requested, strong adverse-versus-clear differences and natural identity continuity.

### 17.6 Added review gate

Before delivery, review hero and supporting character readability at phone size; inspect each person in a multi-person cutout. Check character scale, actual alpha silhouette, clear hierarchy, caption separation, purposeful prop sizes, faint directional illustration shadows, meaningful traced annotations and restored original motion variety. Overlay the supplied red-zone guide through affected movements. Verify the clean export contains no guide. Deliver the matching updated project and this complete additive workflow.

## 18. Biological subjects, micronutrients and chemistry — generated identity labels

When narration names a micronutrient, biological subject, chemical or related scientific entity, generate a recognizable illustration of the actual kind of thing being named. Use a molecular or atomic representation for a nutrient/chemical, a cell or tissue representation for biological structures, and an organism illustration only when the named subject is an organism. Do not substitute a generic fat droplet, pill, mascot or unrelated creature where the molecule or structure itself is the point.

When helpful, include the correct name, chemical symbol or established short label beside the illustration within the same ImageGen generation. The illustration and its identity label must be produced together as one usable image, not as separate generations. For example, use Vitamin C or C for ascorbic acid, Fe for iron, Mg for magnesium, and an accurate named representative when illustrating a class of molecules. Do not invent a symbol such as V for vitamin C.

Keep labels large enough to read, sparse and correctly spelled. Labels are an explicit exception to the general no-baked-lettering default for these scientific identity assets; narration captions remain separately editable. Retain the established red-and-black visual language and true transparency, and attach the normal style references. Where a molecule's bonds, formula, cell morphology or other structure matters, consult an authoritative reference, supply a verified structural reference image when useful, and inspect the generated result for correctness. If a representative molecule stands for a broad class, identify it as an example rather than implying that the class is one single molecule.

These additions preserve all earlier production rules. Apply them to new assets from this point onward; do not regenerate unrelated approved work merely to apply this rule retroactively.


## 19. Sound-effects pack — current required practice

Use `11-Sound-Effects/Sound-Effects-Pack-v2.zip`. Extract it and read its README and Manifest.json; open Listen.html to search and audition. There are 72 named sounds in both WAV and MP3: these are two formats of the same sounds, not 144 distinct effects. The pack includes all three supplied compilations and the original approved project whoosh. Use the 48 kHz, stereo, 24-bit WAV copies for editing; MP3 copies are convenient auditions. Do not regenerate sounds already available here. Preserve source provenance; supplied compilations do not imply a new blanket license.

### 19.1 Choose by action and texture

| Action | Choose and audition | Timing |
| --- | --- | --- |
| Substantial lateral/diagonal entrance or illustration change | Different short whooshes/whips; retain the original whoosh as one variation | Audible sweep follows travel and resolves at settlement. Whooshes must be perceptible, but are not mandatory on every entrance. |
| Small purposeful arrival, contact or reveal | Pop/plop, solid click or short impact | Transient lands on visible contact/settlement. Avoid thin glitchy twitches. |
| Shrink, drain or downshift | Suitable descending/pitch-bend variation tagged shrink | Follow the decrease, ending with the actual motion. |
| Return, reversal or recall | Rewind-like sound or record-scratch where humorous | Use on the reversal, not a random caption change. |
| Successful resolution, emphasis or sparkle | Ting/ding variation | Sparse, precise punctuation; keep ringing tails clear of dialogue. |
| Quiet, soft movement or atmosphere | Soft airy/windy brush | Low enough to leave speech clear; no continuous filler bed. |
| Unlock, tap, mechanism or gear metaphor | Gear/ratchet, especially C01 Gear_Ratchet_Crank_01 | Synchronize visible mechanical action. |
| Comedy, anxiety, friction or a distinct reaction | Appropriate supplied cartoon, vocal, scratch, heartbeat or dry-contact cue | Match the scene's meaning; do not substitute the same pop repeatedly. |

Names and tags are descriptive, not proof of suitability. Audition different candidates in context. Do not invent variations or claim every requested texture is present if the recordings do not contain it. Match a sound's weight to the object's apparent size; alternate suitable variations across scenes.

### 19.2 Align attacks, preserve tails

Use each manifest attack_offset_ms when available: for an intended audible attack at T, start the file near T minus that offset. Verify in the actual mixed playback. Do not align every file start to contact when its audible attack comes later. Keep the effect's beginning, decay and intentional internal pauses intact. If the tail masks the next phrase, choose a shorter appropriate sound or lower its gain; do not casually chop it off. Retiming a movement requires retiming its SFX cue too. Layout-only revisions normally retain approved cue timing.

### 19.3 Audible, solid, speech-safe mix

Do not solve 'too many unnecessary effects' by removing whooshes altogether. Use prominent, purposeful effects with space between meaningful actions. Avoid barely audible ticks, repetitive twitches, excessive sub-bass or a stack of simultaneous decorative noises. Judge at ordinary phone-speaker listening level, not solely on waveforms or headphones. Speech must remain intelligible, including consonants.

The sixth project's working mix is an example, not a fixed template: major whoosh/pop peaks roughly -7 to -10 dBFS, tings -14 to -16, gear about -17 and quiet air about -19 before mastering; brief speech ducking can be around 1–1.5 dB. These numbers depend on the source and overlap. Start by listening and balance the combined mix. Aim around -16 LUFS integrated, with a true-peak ceiling near -1.8 dBTP; measure the encoded delivery too. Leave all summing headroom in a float premaster and prevent clipping. Do not add music unless requested.

Keep the untouched source narration, snapped narration, separate effects track and final mix. Record source ID, path, intended action, attack-aligned onset and gain in sound-cues.json. Include used files and credits in the editable project. Review onsets against movement at normal playback speed, not just held frames.

## 20. Instructor / cane-presenter choreography — current required practice

Read `Instructor-Guide.md`, inspect its three real transparent poses and the sixth reference's final MP4/source. The instructor is an interactive explanatory character, not a fixed sticker. Use him where an explanation benefits, with clear visual hierarchy. Red/black/white identity and bold rounded contours stay consistent.

### 20.1 Entrance, target and retargeting

- Establish the main explanatory object first. Let the instructor enter shortly afterward; avoid mechanically bringing both in at exactly the same instant. A useful offset is about 0.2–0.5 s, adjusted to the phrase and available hold.
- Place the presenter and cane ABOVE the object in compositing order. The cane must be visibly pointing at a meaningful feature, not hidden behind the illustration, stopping in empty space, or merely pointing near its label.
- Measure the actual cane tip in the source PNG. After alpha-bounds fitting, scale, flip, translation and any rotation, register that tip to the chosen screen-space target. Each pose has different geometry: never reuse another pose's tip coordinates blindly.
- When the narration introduces a new prop/feature, START retargeting immediately as that item enters. Do not wait for it to settle, then slowly drift toward it. Use quick controlled travel, roughly 0.2–0.35 s, then a firm hold; the sixth project's moves use 0.28 s. Match object entrance timing where appropriate.
- Reposition, scale and retarget together. Follow upper object → lower object by moving down, potentially enlarging into the bottom corner. Return upward or to center when needed. Preserve the cane's connection to the hand.
- Check both transitions and held frames. The tip must land on the correct current subject at the spoken time. Updating target arrays or passing a coordinate audit does not replace visual checking of what that target represents.

### 20.2 Scale, sides, cropping and spacing

- Make the instructor large and expressive in most explanatory scenes; do not shrink all characters to fit unnecessary props. Scale depends on the current composition, not a fixed percentage.
- A smaller instructor is valid when a detailed bacteria/chart composition needs the space, provided the character remains readable and actually useful.
- Vary left and right placements. For example, insulin/glucose can occupy the right with the presenter on the left; bloodstream or tissue can occupy the left with the presenter bottom right.
- Oversized corner framing is explicitly allowed. The lower body can crop off the bottom/right/left and enter the supplied red zone where intentional. The user accepts partial face visibility for some expressive crops, but keep enough face, the grip and the working cane tip readable. Essential explanatory content and captions still need clear space. A specific user-authorized scientific layout can exceed ordinary safe-area limits.
- Keep substantial negative space between independent silhouettes and their labels. A cane's deliberate pointing contact is meaningful; a sugar bowl touching a stop palm, calendar touching a leg, padlock hiding behind a torso or extra label colliding with a face is not.
- In stacked explanations, raise and space the upper/lower illustrations before shrinking them. Keep one dominant focus. The presenter can move down to the second object, scale and partly leave frame. Do not keep him static while the subject changes.

### 20.3 Poses and expressive behavior

Use the conventional diagonal cane pose when it fits. Also use the approved camera-facing, smirking upward-pointing variations: one has a raised outward grip; the straighter version places the gripping hand beside the face with the cane vertical, a small gap from the head and a slight head tilt away from the cane. The other hand stays on the hip. Inspect hand anatomy and keep a natural connected grip. Use a mirrored pose only if it suits the composition and does not reverse important text. Do not rotate an entire upright figure unnaturally just to aim the cane.

### 20.4 Relevant micro animations and holds

Keep explanatory context in place while the meaningful part changes. Animate graph lines along their true paths; maintain a shared baseline and readable width (the revised sugar graph spans about 80% of the canvas). Give complex explanations enough time by borrowing an earlier excessive hold where possible, without changing narration or misaligning phrases.

If material emerges from a tank/nozzle, anchor it to that nozzle: start tiny/nearly invisible, drop out and expand into a distinct readable illustration. Do not add a disconnected line, dot or duplicate caption without explanatory purpose. As other elements leave, let the retained main subject become larger and rise, with the instructor scaling/repositioning to maintain accurate pointing. Clear outgoing props promptly before they overlap new coherent hand-held acting.

## 21. Portable workspace and reference precedence

The six finished project references are Protect Their Peace, When He Goes Quiet (Clean Fades), Braces or Aligners Part 3, Remea Gut to Glass, Walking — The Magic Pill (Vertical Gauge), and Sugar — Two Weeks (final nineteen-fix revision with straight-cane head tilt). Supporting original style video and micro-explanation excerpts are additional study material, not extra project counts.

For new work read this complete workflow, Animation-Sheet.md, OG-MOTION-STUDY.md, Micro-Explanation-Animation-Study.md, Instructor-Guide.md and Sound-Effects-Usage.md. Study the six MP4s and relevant editable sources. Project 6 is the latest instructor/spacing benchmark; older references remain useful for original choreography and composition. Explicit new user directions take precedence. Old workflow copies nested in historical project ZIPs are historical and must not override this top-level workflow. Use supplied narration unchanged except carefully protected silence tightening; do not generate replacement takes without authorization.

Asset count follows the current script and user brief. Their requested 60+, 70+ or 85+ counts are project-specific, not reasons to crowd each scene. Count reusable assets only when they precisely depict the matched phrase. Distinguish independent props from coherent hand-held/body-contact illustrations: the approved man holding a plate remains one illustration; independently arriving sugar/calendar are separate layers.

Keep all necessary source, actual style references, art, timing, fonts, scripts, audio and reproduction notes locally portable. Record progress after each expensive generation batch and major edit. A preview link or unsaved tool output is not a checkpoint. Preserve final downloads plus editable ZIP. Clean packaging may exclude interrupted temporary files and exact duplicate renders, but never omit unique approved artwork or final media. Standard ZIP compression is lossless; already compressed PNG/MP4/MP3 data may shrink little. Avoid lossy recompression solely to meet a smaller package size.


## 22. Additive updates and compact reference videos — explicit user rule

Whenever updating this workflow, retain ALL existing information. Append new rules, clarifications and dated amendments; do not delete, silently replace or summarize away earlier sections. If a new user instruction supersedes an older one, append a narrowly scoped explanation of which rule changes and why. Keep the two full workflow filenames synchronized. Existing historical instructions remain visible.

For this six-reference workspace pack, the user explicitly requested compact finished-video references of around 5 MB each. These are 720×1280, 30 fps H264 viewing copies with AAC audio, made using two-pass encoding. This is a specific exception to the no-lossy-recompression packaging preference in section 21. The compact videos preserve the full scene sequence and duration but are NOT bit-identical or visually lossless masters. Do not describe them as full-quality final exports. Use the complete editable projects, original-resolution artwork and source audio to inspect fine details and render at full quality. The separately delivered finished Sugar video is unchanged.

Only unused interrupted temporary transfers and an exact duplicate export may be removed from the package when they are irrelevant to understanding/reproducing the project. Preserve all meaningful source, assets, timing, documentation, required media and provenance. Do not let a size target justify removing unique reference material. Supporting micro-explanation source clips and original motion reference remain as supplied.


## 23. Rendered reference video must also be inside every project ZIP

Explicit user clarification: each reference project's editable ZIP MUST contain its corresponding complete rendered MP4. In this workspace, all six inner project ZIPs include the same compact ~5 MB 720×1280, 30 fps MP4 that appears beside the ZIP, under the project folder's renders/ directory. Compress both locations consistently by encoding once and copying the identical bytes. Do not remove the embedded render merely because an outside copy exists. This overrides the duplicate-render cleanup allowance in sections 21–22 for these required deliverables. Temporary interrupted files remain removable when unused. Full-resolution editable art/source audio remain included; compact reference videos are lossy viewing copies, not master-quality exports. See PROJECT-RENDERS-INDEX.json for exact member paths.


## 24. Browsable repository, seventh reference and bouncy UI study — 30 October 2026

This dated clarification supersedes only the six-reference count, duplicate-workflow filename synchronization and outer-ZIP setup instructions in sections 21–23. All earlier production guidance is preserved above.

### 24.1 One authoritative workflow and individually accessible components

`04-Workflow-and-Animation/workflow.md` is the ONLY current standalone workflow. The former `Stickman Animations Workflow.md` compatibility copy is consolidated into it. The source workflow and the supplied Iron–Oxygen final project's workflow snapshot were compared and are byte-identical (74,952 bytes); no newer version was found in those sources. Append future dated amendments here while preserving earlier information. Workflow copies sealed inside unchanged historical project ZIPs are project records and must not override this file.

The first cover of the old 383 MB workspace ZIP has been opened into individually browsable numbered folders and files at the repository root. All individual editable project ZIPs remain intact. The old v1.0.0 release and archive metadata are historical, not a requirement for current setup. Import ALL current repository files, including real Git LFS contents. Follow the current README, START-HERE and STUDY-CATALOG. Verify the current manifest, extract all seven editable projects into separate working locations, and preserve their internal paths.

### 24.2 Seven finished references

Reference 7 is **Iron, Oxygen and Real Energy**, at `12-Project-7-Iron-Oxygen-Real-Energy/`. Use the supplied final original-art edit with finishing polish. Its ZIP and embedded video are preserved unchanged; the same complete MP4 is also accessible beside the ZIP. Study scientific illustrations, retained-subject handoffs, instructor target registration/retargeting, UI sequences, phrase timing and motivated sound through actual playback and editable source. The seventh reference supplements the existing six. Project 6 remains the documented instructor/spacing benchmark unless a current brief specifies otherwise. References 1–6 keep their compact viewing copies; reference 7 keeps its supplied 1080×1920, 30 fps, 94.8-second render without recompression.

### 24.3 Separate bouncy animation study

In `13-Bouncy-Animation-Study/`, read Bouncy-Study-README.md, Bouncy-UI-Animation.md, Bouncy-UI-3D-Addendum.md and the editable project's README/DESIGN. Inspect its HTML/GSAP source, local dependencies, effect-generation source and verification reports. Watch the current 22-second three-scene dimensional demo, the source compilation, all three original excerpts and the previous nine-second sample for comparison. The previous sample is historical, not the current demo. Supporting studies do not increase the seven-project reference count.

Use dimensional UI objects, controlled spring response, staggered cascades, contact shadows and connected transitions deliberately where the current brief calls for them. This study does not globally replace the stickman palette or require every illustration to bounce continuously. Preserve accurate narration timing, readable holds, hierarchy and instructor targeting. Original reference excerpts and the newly authored demonstration remain separately identified; preserve provenance.

### 24.4 Deep setup and study

Import and verify every current component. Read the ENTIRE workflow and all current animation, micro-explanation, instructor, sound and bouncy guides. Inspect actual style images and poses. Extract all seven source projects, visual references and the sound pack; read all included documentation and understand the source, design, storyboard, art, captions, narration, timings, sound cues and QA records. Review all seven full videos with sound, the original-motion reference and every micro-explanation/bouncy excerpt. Inspect both held frames and transitions, and audition effects.

Record a phrase/time/source map for every sample: meaning, acting, hierarchy, layers, captions, movement/holds/exits, retained context, changing scientific parts, pointer targets, retarget timing and audible effect attacks/tails. A file inventory is not audiovisual study. Mark what was actually read, watched, heard, inspected or run; report unavailable media/tools instead of claiming completion. Then plan the CURRENT user's script, recording and brief. Preserve narration and word endings, reduce clutter, vary purposeful motion, and keep source and final outputs portable.


## 25. Individual oversized project downloads — 30 October 2026

The account's exhausted Git LFS budget prevents the LFS distribution planned in section 24. This narrowly supersedes that section's LFS import instruction. No paid storage change was authorized or made.

All ordinary ZIPs, videos, documents, studies, references and the complete sound library are directly in Git. Only the two whole ZIPs above GitHub's normal 100 MB limit (references 6 and 7) are separately downloadable release assets. They are linked from their individual project folders and root DOWNLOADS.md. They are NOT split into parts, recompressed or placed in a bulky outer bundle. Their contents and embedded renders remain unchanged.

After cloning, run `python3 tools/fetch_large_projects.py` to download just those two whole ZIPs into their normal folders with checksum verification, then run `python3 tools/verify_workspace.py`. Manual downloads to the documented paths are equally valid. A source-code-only download is incomplete until those two project ZIPs are imported. The manifest records their exact bytes, hashes and individual download URLs. No Git LFS is required. All full-study and preservation requirements above remain in force.


## 26. All project ZIPs directly in Git — lossless packing, 30 October 2026

The user prefers every individual project listed as a normal repository file and explicitly requested compression. This supersedes section 25's release-download setup and section 24's proposed Git LFS setup. ALL SEVEN editable project ZIPs are now ordinary files in their project folders. No separate fetch helper, Git LFS or bulky outer workspace ZIP is required.

References 6 and 7 are repacked using lossless FLAC storage for three large working WAV tracks and lossless WebP storage for selected PNGs. No illustrations, source code, narration, timing, sound cues or finished videos are removed. Image pixels including alpha and original resolution are preserved; complete finished MP4s are byte-identical to the original renders and remain inside/beside each ZIP. The older unoptimized ZIPs remain in release v1.1.0 only as historical backups. Their old byte checksums describe those backups, not the new packed ZIPs.

After extracting either compact project, install its normal dependencies including Pillow and FFmpeg and run `python restore_assets.py` from the extracted project folder BEFORE source preview/editing. This restores original working WAV files byte-for-byte, including their headers, and pixel-identical PNGs to their original paths. Read the bundled README and LOSSLESS-COMPRESSION.json; the existing source/build/render scripts then use their normal paths. The finished MP4s play immediately without restoration. Do not claim PNG file encodings are byte-identical: their pixels are exact, while the PNG encoding can differ.

Both complete unpack-and-restore paths were tested. Audio full-file SHA-256, original-resolution RGBA pixels including transparent RGB/alpha, unchanged source members and the exact embedded/outside videos were verified. Current root manifests and archive indexes describe the new packages. All earlier full-study, sound-library, original-motion, micro-explanation, instructor, bouncy-study and preservation requirements remain in force.
