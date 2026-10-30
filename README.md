# Stickman Video Workflow — seven references

A browsable red/black/white stickman-video workspace with **seven finished reference projects**, individually listed editable ZIPs and matching videos, one current workflow, micro-explanation studies/clips, instructor references, the complete 72-effect sound pack and the dimensional bouncy UI study.

The bulky outer workspace ZIP is no longer needed for a current setup. Its components are listed directly here; individual project ZIPs remain intact. The original six-reference v1.0.0 release remains an archival snapshot.

## Get the entire current workspace

```bash
git clone https://github.com/Gregokeke/stickman-video-workflow.git
cd stickman-video-workflow
python3 tools/verify_workspace.py
```

**Every project ZIP is now a normal file in its project folder.** No Git LFS, separate release download, fetch helper or bulky outer ZIP is required. [DOWNLOADS.md](DOWNLOADS.md) links all seven project ZIPs directly.

References 6 and 7 use compact lossless asset storage to fit GitHub's file limit. After extracting either project, install its normal dependencies (including Pillow and FFmpeg) and run `python restore_assets.py` before previewing/editing. This restores byte-identical WAV tracks and pixel-identical PNGs at their original resolution. Source script paths then work normally. Their complete finished MP4s are unchanged and play immediately without restoration. See [LOSSLESS-PACKAGING.json](LOSSLESS-PACKAGING.json) for measured sizes and validation.

Read [START-HERE.md](START-HERE.md), the ENTIRE [current workflow](04-Workflow-and-Animation/workflow.md), and [STUDY-CATALOG.md](STUDY-CATALOG.md). Import and analyze **every current component**, including all seven editable source projects and actual video/audio. Listing files or skimming guides is not deep study.

## Seven finished sample references

Every project has an individual editable ZIP and the matching complete rendered MP4. All seven ZIPs are stored directly in their folders as ordinary files. Each ZIP also contains that same MP4 internally. Preserve relative paths when extracting.

| # | Project | Study focus |
| --- | --- | --- |
| 1 | [Protect Their Peace](02-Project-1-Protect-Their-Peace/) | Foundational acting, motion and content style. |
| 2 | [When He Goes Quiet — Clean Fades](03-Project-2-When-He-Goes-Quiet/) | Connected movement, hierarchy, early outgoing fades and meaningful retained context. |
| 3 | [Braces or Aligners Part 3](06-Project-3-Braces-or-Aligners-Part-3/) | Illustration choreography and solid, motivated sound. |
| 4 | [Remea Gut to Glass](07-Project-4-Remea-Gut-to-Glass/) | Scientific explanations, expressive characters and clear compositions. |
| 5 | [Walking — The Magic Pill](08-Project-5-Walking-The-Magic-Pill/) | Final Vertical Gauge revision, detailed phrase coverage and micro explanations. |
| 6 | [Sugar — Two Weeks](10-Project-6-Sugar-Two-Weeks/) | Final nineteen-fix revision, straight-cane head tilt, precise targets, immediate retargeting, spacing and sound. |
| 7 | [Iron, Oxygen and Real Energy](12-Project-7-Iron-Oxygen-Real-Energy/) | Supplied final original-art edit with finishing polish, scientific handoffs, presenters and UI sequences. |

References 1–6 retain their original compact ~5 MB, 720×1280, 30 fps lossy viewing copies. Complete editable artwork/audio remain inside their projects. Reference 7 retains its supplied 1080×1920, 30 fps, 94.8-second final render without recompression. Reference scripts are not narration sources for unrelated new videos.

## Documents and supporting references

| Component | Direct entry |
| --- | --- |
| Single authoritative workflow | [workflow.md](04-Workflow-and-Animation/workflow.md), all sections and dated clarifications. |
| Animation sheet | [Animation-Sheet.md](04-Workflow-and-Animation/Animation-Sheet.md) |
| Original motion study | [OG-MOTION-STUDY.md](04-Workflow-and-Animation/OG-MOTION-STUDY.md) |
| Original uploaded motion video | [Original-Reference.mp4](01-Original-Video-Reference/Original-Reference.mp4) |
| Micro-explanation study | [Micro-Explanation-Animation-Study.md](04-Workflow-and-Animation/Micro-Explanation-Animation-Study.md) |
| All three micro-explanation source clips | [Clips and index](09-Micro-Explanation-Reference-Clips/) |
| Instructor guide | [Instructor-Guide.md](04-Workflow-and-Animation/Instructor-Guide.md) |
| Instructor poses and scene examples | [Instructor references](04-Workflow-and-Animation/references/instructor/) |
| Actual supplied visual-reference images | [05-Visual-References.zip](05-Visual-References.zip), extract into `04-Workflow-and-Animation/`. |
| Red-zone review canvas | [red-zone-canvas.png](04-Workflow-and-Animation/references/red-zone-canvas.png) |
| Sound-effects practice | [Sound-Effects-Usage.md](04-Workflow-and-Animation/Sound-Effects-Usage.md) |
| Complete sound-effects library | [Sound-Effects-Pack-v2.zip](11-Sound-Effects/Sound-Effects-Pack-v2.zip), including documentation, index, manifest, audition page and 72 WAV/MP3 pairs. |
| Bouncy UI reference study | [Bouncy-UI-Animation.md](13-Bouncy-Animation-Study/Bouncy-UI-Animation.md) |
| Dimensional / 3D motion addendum | [Bouncy-UI-3D-Addendum.md](13-Bouncy-Animation-Study/Bouncy-UI-3D-Addendum.md) |
| Current three-scene bouncy demonstration | [Bouncy-UI-3D-Demo.mp4](13-Bouncy-Animation-Study/Bouncy-UI-3D-Demo.mp4) |
| Bouncy source clips, compilation, editable project and verification | [Complete study folder](13-Bouncy-Animation-Study/) |

Supporting footage and UI demos are studies, not additional numbered finished-project references. The prior nine-second UI sample remains for comparison. Use depth/spring treatments purposefully for suitable UI or prop moments, while preserving stickman art direction, readable holds, narration timing and accurate presenter targets.

## Required workspace setup and deep study

1. **Import everything and verify.** Bring every component in the current manifest, including all seven ordinary project ZIPs. Read START-HERE and the complete workflow; historical package metadata explains provenance and does not govern new production.
2. **Read all current guides completely.** Study animation, original motion, micro explanations, instructor choreography, sound and both bouncy documents. Extract visual references and inspect the actual JPGs, instructor poses, scene examples and red-zone guide. Attach real style images during generation.
3. **Open all seven editable projects.** Extract into separate writable folders and read every included README/design/production note. Understand the complete storyboards, build/animation/mix/render code, source art, asset provenance, narration, captions, words, timing and sound cues. Inspect the bouncy editable source too. File names and implementations differ; follow each project's own README and lockfile.
4. **Study actual media with sound.** Review every complete project video, the original motion reference, all three micro-explanation clips, the bouncy compilation and all three source excerpts, the current 22-second demo and the old sample for comparison. Inspect important held frames and transitions by scrubbing. Extract and audition the complete sound pack; WAV/MP3 are two formats of the same 72 effects.
5. **Demonstrate understanding.** Record a phrase/time/source map for every finished sample: narrated meaning and acting, hierarchy, layers, captions, movement paths/holds/exits, retained context, scientific changes, pointer targets, retarget timing and audible effect attacks/tails. Explain each reference's distinct contribution; avoid applying one repeated animation recipe everywhere.
6. **Establish the runtime.** Follow each project's actual install/preview instructions and lockfile. Verify Node, required Python packages, FFmpeg/ffprobe and browser/runtime access. Existing packaged art/audio suffice for studying references; do not regenerate speech or art merely to preview them.
7. **Then plan the current brief.** Use the user's CURRENT script/recording, illustration count and authorized reuse. Preserve supplied narration and word endings, reduce clutter, vary fluid purposeful motion, use helpful micro explanations and precise instructors, and review actual mixed playback and final encoded output.

Record what was actually read, watched, heard, inspected or run. Resolve missing material or capabilities before claiming setup is complete. See [STUDY-CATALOG.md](STUDY-CATALOG.md) for the checklist and [FILE-INDEX.md](FILE-INDEX.md) for every current file and archive member. An inventory alone is not study.

## One current workflow and preservation

`04-Workflow-and-Animation/workflow.md` is the only authoritative standalone workflow. The old long-name duplicate is consolidated. The workflow inside the supplied seventh project matched the old top-level version exactly; the current document preserves that entire text and appends dated repository/seventh-reference/bouncy guidance. Historical workflow copies sealed inside unchanged project ZIPs are project records and must not override it. Append future workflow updates while preserving earlier information. Explicit current user instructions take precedence.

The first five editable ZIPs, all seven embedded/outside videos, the visual-reference ZIP and complete sound pack are preserved byte-for-byte. References 6 and 7 are repacked with lossless image/audio storage: their original-resolution pixels, audio samples, source material, timing and complete videos are preserved. Their unoptimized original archives remain in release v1.1.0 as historical backups, not setup requirements. The bouncy study is exposed as individual documents, media and source files. The redundant standalone workflow alias is consolidated into the single current workflow; its complete original text is retained, with an exact historical copy inside reference 7. The original transfer fragment is retained only as historical material under `archive-metadata/v1.0.0/`. Historical package reports are retained under [archive-metadata/v1.0.0](archive-metadata/v1.0.0/).

## Integrity and rights

[PACKAGE-MANIFEST.json](PACKAGE-MANIFEST.json) contains current file sizes/checksums; [PROJECT-RENDERS-INDEX.json](PROJECT-RENDERS-INDEX.json) records all seven embedded/outside render pairs; [ARCHIVE-CONTENTS.json](ARCHIVE-CONTENTS.json) lists every ZIP member. Run `python3 tools/verify_workspace.py` after import and packaging changes.

This is the user's production workspace, not a blanket open-source license for enclosed images, voices, source clips or sound compilations. Preserve provenance and credits. The user explicitly authorized publishing this prepared layout to the existing public repository; that does not authorize unrelated redistribution or future visibility changes.

The final [original-content audit](ORIGINAL-CONTENT-AUDIT.json) accounts for all 47 original outer-archive entries, checks every original member of the two losslessly repacked projects, and confirms the complete sound library. Original package metadata remains available under its labeled archival folder.
