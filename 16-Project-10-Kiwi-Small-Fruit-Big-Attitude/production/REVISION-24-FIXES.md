# Latest follow-up supersedes earlier cutting/pause details

Fruit holder raised90px and scaled1.025; upper horizontal scissors cut and upper/lower protein split; C-curved arrow draws during cut; no cut instructor;600ms added silence removed. Final114.6s/3438frames. All other illustrations preserved.

# Kiwi — 24 precision fixes

Final revision:115.2seconds,1080×1920,30fps. All timings refer to the revised narration. The only added time is600ms of silence at100.000s, after the recorded word “proteins” ends99.851s. Every sample from the previously approved tightened voiceover is retained in order. The next sentence begins100.771s.

| # | Requested change | Final implementation |
| --- | --- | --- |
| 1 | Spider clear of avatar; bigger abdomen | Targeted edit enlarges rear abdomen. Spider moved to upper-left; held alpha bounds have a visible vertical gap from avatar. |
| 2 | Diagonal animated VS slash | Separate V/S and diagonal slash. Slash is hidden until its actual draw cue, then draws over340ms. |
| 3 | Boxing gestures | Offset finite lean/lunge/recoil actions for both kiwi instances and orange; deliberate upper staging makes space for referee. |
| 4 | Referee on “although” | Entry starts12.744s, with casual tilts and small scale/body movements. |
| 5 | Potassium, heart character and trace | Potassium raised; exact approved heart-holding character enlarged/lowered. Pulse trace moved beside potassium, draws and pulses. |
| 6 | Vitamin E staging and gauge | Large waist-cropped fruit-holding character; larger standalone vitamin E. Upper-left gauge drains on “zero”; numeric0 appears. Slash draws on spoken vitamin E after gauge empties. |
| 7 | Rusting illustration | Unnecessary red overlay removed. Large lower instructor retargets from membrane to damaged membrane on “rusting,” with waist crop and readable face. |
| 8 | Kiwi transition | Character kiwi clears fully before normal kiwi-half entry. |
| 9 | Purposeful bold drawn lines | Kept routes have12px or stronger strokes, explicit hidden initial states and visible draw cues. Arrowhead strokes start from their connected shaft endpoint. |
| 10 | Tragic gut setup | Removed the separate intestine prop from this setup. Existing belly-holding actor receives a slight scale emphasis on “gut.” |
| 11 | Water absorption | Drop follows a staged descent; offset trail visibly draws/retracts. Sponge scales on landing. Separate instructor precisely tracks fiber, drop and landing point. |
| 12 | Gut sweep | White bold trace follows actual open colon lumen to its outlet; a tracked bolus and finite dirt sweep complete the explanation. Instructor follows the path. |
| 13 | Constipation chart instructor | Larger lower instructor with readable face and bottom crop; controlled pointer rise stops below the bar top. Head stays below chart. |
| 14 | Discomfort and comfort | Discomfort stays on left; comfort enters/stays on right. Both remain below the chart until shot handoff. |
| 15 | Brain, pineal, melatonin | Instructor targets serotonin, moves down to entering brain, returns to pineal, then lowers to larger melatonin. Extra curve removed; downward arrow retained. |
| 16 | Awake in bed | Overlay line removed. Small scale emphasis on “ceiling.” |
| 17 | Gym/glucose | Glucose enlarged and moved up-right, clear of avatar and captions. |
| 18 | Muscle fuel | Bold accurately connected drawn glucose-to-muscle arrow with finite arrival emphasis on muscle. |
| 19 | Fiber to enzyme | Snappy pointer targets fiber under graph, then rapidly moves to enzyme at its entry. |
| 20 | High scissors and side switch | Scissors raised/left, with measurable gap from enzyme. Instructor switches to opposite side and points at scissors; clears before stomach becomes fully visible. |
| 21 | Physical protein cut | Scissors persist, accelerate through protein and continue fully off-screen as their exit. Original protein PNG is independently clipped into two geometric halves that separate and remain visible. |
| 22 | Delayed peptide arrow/reveal | Instructor clears before a single curved arrow draws. Connected arrowhead completes; peptides then enter. No red cut overlay.600ms silence gives the completed explanation a readable hold. |
| 23 | Wet brick | Unnecessary slash removed. |
| 24 | Sad underrated kiwi | Targeted new pose: downcast open eyes, sad mouth, hunched/slouched body and lowered boxing gloves. Same fuzzy red/black identity, small legs and red shoes. |

## Follow-up clarification

Scissors slicing and exit are one continuous movement. There is no separate exit reversal or in-place fade. Split protein halves remain while the curved arrow draws toward the appearing peptides.

## Checks

- Master timeline is deterministic and seekable. Frame review checks exact pointer registration, captions, image loading and requested event ordering.
- Original tightened narration compared sample-for-sample against revised narration with the inserted silence removed; all original samples are identical.
- Browser check includes runtime/layout/motion/contrast/audio and craft review. Dense wrapper/duplicate-source warnings are expected for independent appearances and clipped protein halves. Fast caption warnings follow the supplied voice.
- Full encoded MP4 decode and decoded AAC/master comparison are recorded in adjacent verification JSON files.
- Intentional lower-body/side instructor crops and the requested large fruit-holder crop are permitted framing; faces, grips and working tips remain readable.

## Editing

Final authoritative files are `storyboard.json`, `animation.js`, `revision-motion.js`, `micro.html`, `micro.css`, `micro.js`, `words.json`, `captions.json` and the saved final narration/mix. Run `python3 build.py`, then the documented render. Original intake scripts are optional; normal visual changes do not require regenerating audio or transcription.
