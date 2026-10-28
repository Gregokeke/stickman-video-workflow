# Stickman Video Workflow

A portable red, black and white stickman-video production workspace: the full additive workflow, six finished HyperFrames reference projects, compact rendered examples, micro-explanation studies, precise instructor choreography and the complete 72-effect sound pack.

**Repository description:** Red/black stickman video workflow with six editable references, precise instructor animations, micro-explainers and a 72-effect sound pack.

## Get the actual workspace

The 383 MB workspace ZIP is distributed as a **GitHub Release attachment**, rather than a normal Git file. Cloning the repository alone gives you this README, not the reference media. Download the named attachment from Releases; GitHub's automatically generated “Source code” ZIP is not the workspace pack.

For an agent with authenticated GitHub CLI access:

```bash
gh release download v1.0.0 \
  --repo Gregokeke/stickman-video-workflow \
  --pattern Stickman-Animations-Workspace-6-References.zip \
  --dir workspace-download
```

For a private repository, the agent/account must have access to this repository and its release assets. Importing a repository into a different workspace does not automatically authorize a separate GitHub identity. Do not request or print access tokens in chat.

Expected attachment:

- Name: `Stickman-Animations-Workspace-6-References.zip`
- Size: `383125626` bytes
- SHA-256: `78a71d7e9f62d521f0e01acb56652d7f17cb66cfd7e779e4bf5fcd20101a8199`

Verify and extract:

```bash
python - <<'PY'
from pathlib import Path
import hashlib, zipfile
p = Path('workspace-download/Stickman-Animations-Workspace-6-References.zip')
assert p.stat().st_size == 383125626
assert hashlib.sha256(p.read_bytes()).hexdigest() == '78a71d7e9f62d521f0e01acb56652d7f17cb66cfd7e779e4bf5fcd20101a8199'
with zipfile.ZipFile(p) as z:
    assert z.testzip() is None
    z.extractall('workspace')
PY
```

The extracted folder is `workspace/Stickman-Animations-Complete-Workspace/`. Paths below are relative to that folder.

## Agent: read and study before starting a video

1. Read `START-HERE.md`.
2. Read the ENTIRE `04-Workflow-and-Animation/workflow.md`. The longer filename `Stickman Animations Workflow.md` is its byte-identical compatibility copy. Do not treat either as a summary.
3. In the same folder, read `Animation-Sheet.md`, `OG-MOTION-STUDY.md`, `Micro-Explanation-Animation-Study.md`, `Instructor-Guide.md` and `Sound-Effects-Usage.md`.
4. Extract `05-Visual-References.zip` into `04-Workflow-and-Animation/`. Inspect the actual style images and red-zone guide; attach actual references to illustration generation.
5. Study all six finished videos and the relevant editable sources. Watch the original motion reference and the three micro-explanation source excerpts. Do not claim to have watched material that you have only inventoried.
6. Extract `11-Sound-Effects/Sound-Effects-Pack-v2.zip`. Read its README, index and manifest, and audition with `Listen.html`. WAV and MP3 are two formats of the same 72 sounds. The original whoosh is included.
7. Only then plan the current supplied narration phrase by phrase. Follow the user's current brief, requested illustration count and authorized reuse. Do not copy another reference's script.

## Package map

| Folder/file | Purpose |
| --- | --- |
| `01-Original-Video-Reference/` | Foundational uploaded motion/style video. |
| `02-Project-1-Protect-Their-Peace/` | First finished reference and editable source ZIP. |
| `03-Project-2-When-He-Goes-Quiet/` | Clean Fades revision; connected motion, hierarchy and early outgoing fades. |
| `04-Workflow-and-Animation/` | Authoritative full workflow, studies, guides, red-zone canvas, instructor poses and scene examples. |
| `05-Visual-References.zip` | Actual supplied style images and reference-selection guide. |
| `06-Project-3-Braces-or-Aligners-Part-3/` | Braces reference, animation and sound craft. |
| `07-Project-4-Remea-Gut-to-Glass/` | Scientific content and clear explanatory compositions. |
| `08-Project-5-Walking-The-Magic-Pill/` | Final Vertical Gauge revision, 125.1 seconds. |
| `09-Micro-Explanation-Reference-Clips/` | Three indexed demonstration excerpts. |
| `10-Project-6-Sugar-Two-Weeks/` | Latest 123.166667-second reference: final nineteen-fix revision with straight-cane head tilt. |
| `11-Sound-Effects/` | Complete sound pack ZIP and entry note. |
| `PACKAGE-MANIFEST.json` | File sizes and checksums. |
| `PROJECT-RENDERS-INDEX.json` | Exact embedded render paths for all six projects. |
| `REFERENCE-VIDEO-COMPRESSION.json` | Compact video encoding details. |
| `PACKAGE-COMPRESSION-REPORT.json` | Source-archive cleanup/compression record. |

Each project folder contains an editable ZIP and a rendered MP4. Each editable ZIP ALSO contains that same rendered MP4 under its own `renders/` directory. Extract the inner project ZIP before inspecting or running its source. Preserve relative paths and follow its README; do not assume dependencies or browser/runtime tools are already installed.

Reference videos are compact ~5 MB, 720×1280, 30 fps viewing copies. They are lossy previews of the complete sequence, not master-quality exports. Original-resolution artwork and editable source audio remain available for close inspection and full-quality rendering. The original motion reference and micro-explanation clips remain supporting material, not extra finished-project counts.

## Rules that must survive every new workspace

- **Workflow updates are additive:** preserve all existing information and append new instructions. If a later instruction supersedes an older one, append a precise clarification; never silently delete the older section. Keep both workflow filenames synchronized.
- Use the red/black/white stickman art direction in this pack. Do not import unrelated avatar styles or generic defaults.
- Phrase-accurate illustration and reuse; clear hierarchy; large expressive actors; no redundant tiny props or clutter. Coherent hand-held/body-contact acting may be one illustration; independently moving props need separate layers.
- Fluid move → stick → move choreography, purposeful holds, varied side/center returns and clean handoffs.
- Instructors enter shortly after the main explanation, point at an actual feature, retarget immediately and snappily as the next object enters, and stay visibly above the explained art. Vary sides and scale. Intentional large corner crops are allowed as detailed in the workflow. Use Project 6 and the instructor guide as the latest benchmark.
- Use micro explanations only when they help; retain context and animate the changing part. Keep diagrams and scientific imagery in the established palette.
- Use the supplied sound pack precisely: prominent, solid, varied, action-aligned effects with protected attacks/tails and clear speech. Selective audible whooshes remain part of the style. No music by default.
- Preserve supplied narration and word endings while tightening actual silence. Do not regenerate speech merely to preview or render an existing project.
- Check held frames AND transitions, cane-tip alignment, caption timing, actual mixed playback and final encoded output. Save durable progress after expensive generation batches and major edits.
- Historical workflow copies inside old projects do not override the current top-level workflow. Explicit new user instructions take precedence.

## Rights and distribution

This is the user's production workspace, not a blanket open-source license for the enclosed images, voices, source clips or sound compilations. Preserve included provenance and credits. Keep the repository private unless the user explicitly authorizes public distribution.
