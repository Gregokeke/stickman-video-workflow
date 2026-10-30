# Bouncy UI — dimensional demo

22 seconds, three scenes, 1080 × 1920, 60 fps. Clock selection and falling tags, a dimensional time-card cascade, then an original rhythm sculpture.

See the two Markdown guides in the parent folder. The bundled font, GSAP runtime and generated effects make the project locally self-contained. Node 22+, FFmpeg and the HyperFrames browser are needed for rendering.

```
npm ci
npm run check
npm run dev
npm run render -- --fps 60 --quality high --output Bouncy-UI-3D-Demo.mp4
```

The HTML registers a paused GSAP root timeline. Use HyperFrames Studio to play or scrub; raw HTML intentionally stays paused. All sources are editable in index.html. Rounded depth slices create object thickness; changing perspective and parent rotation reveals it. Object-specific highlights and independent stage shadows support the dimensional look. Sound is original synthesized audio. Source reference audio is included only in the separate reference clips.

The final half-second fades gently. The title begins at 0.1 seconds; choose a later hero frame for a thumbnail. The project has no required online visual assets.
