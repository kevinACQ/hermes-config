---
name: creative-production-workflows
description: "Creative production across ASCII art/video, Manim explainers, p5.js generative art, and browser typography demos; includes concept, rendering, export, and visual QA."
version: 1.0.0
author: Hermes Agent
license: MIT
platforms: [linux, macos, windows]
metadata:
  hermes:
    tags: [creative, ascii-art, ascii-video, manim, p5js, generative-art, typography, pretext, animation, video]
---

# Creative Production Workflows

Use this umbrella for programmatic visual work spanning text art, animation, generative browser sketches, educational cinema, and kinetic typography. Route first by medium, then apply the shared production standard.

## Medium Router

| Desired artifact | Primary workflow |
|---|---|
| Static terminal banner, decorative frame, image-to-text conversion | ASCII art |
| Animated character-grid video or audio-reactive text visuals | ASCII video |
| Mathematical, algorithmic, or technical explainer | Manim |
| Interactive or generative browser canvas, shaders, 2D/3D art | p5.js |
| Prose flowing around geometry, per-glyph physics, text-as-game geometry | Pretext |

Use specialized standalone skills when the task is principally ComfyUI lifecycle/workflow execution or live TouchDesigner control; those are complete operational integrations rather than merely output media.

## Shared Creative Standard

Before coding, state the concept in concrete terms:

- viewer emotion and atmosphere;
- visual story or interaction arc;
- color world and contrast hierarchy;
- shape or character vocabulary;
- motion and transition vocabulary;
- one project-specific invention that prevents tutorial-grade output.

Then define resolution/aspect ratio, frame rate or interaction model, export target, performance budget, and verification method. Prefer a cohesive system of three related effects over ten unrelated effects. Build hierarchy with opacity, scale, motion, and density. Never treat a successful render as proof of a successful design.

## 1. Static ASCII Art

Route by need:

- text banner → `pyfiglet` or a FIGlet-compatible API;
- character speech bubble → `cowsay`;
- decorative border → `boxes`;
- terminal color effects → `toilet`;
- image conversion → `ascii-image-converter` or `jp2a`;
- QR/weather utilities → direct text-returning services;
- custom scene → manually composed Unicode and box-drawing characters.

Keep terminal-safe output roughly within 60 columns unless the user requests a wider canvas. Preview multiple fonts for short titles, preserve signatures on sourced artwork, and verify alignment in a monospace renderer. ANSI color is terminal-specific and should not be assumed to survive plain files or chat transports.

## 2. ASCII Video

Use the pipeline:

```text
INPUT → ANALYZE → SCENE → TONEMAP → SHADE → ENCODE
```

Inputs may be source video, audio features, procedural fields, timed text, or hybrids. Compose multiple character-grid densities and vary palette, hue, background field, particles, and shader intensity by scene while maintaining a shared aesthetic.

Critical implementation rules:

- normalize brightness with percentile-based tonemapping rather than linear multipliers;
- use screen-style blending for dark layers;
- validate Unicode glyph support in the chosen font;
- derive cell height from font metrics when raster APIs report incorrect bounds;
- do not pipe long-running ffmpeg stderr into an unread buffer;
- render key test frames before the full video;
- use per-clip rendering for selective rerenders and parallel work.

Verify frame brightness, visual coherence, encoding, audio sync, and final dimensions.

## 3. Manim Educational Video

Start with the teaching arc: misconception, visual intuition, formalization, and the “aha” reveal. Show geometry before algebra where possible.

Recommended project shape:

```text
plan.md
script.py          # one independently renderable class per scene
concat.txt
final.mp4
media/
```

Use low-quality draft renders for iteration and production quality only at the end. Maintain shared color constants, monospace text for reliable Pango layout, minimum readable font sizes, explicit pauses after key reveals, and opacity layers that separate context from focus. Use raw strings for LaTeX and cleanly remove or transform old objects before introducing replacements.

Verify preview stills, scene pacing, equation correctness, clipping near frame edges, subtitle timing, and final ffmpeg stitching.

## 4. p5.js Generative and Interactive Art

Default to one self-contained HTML file unless the project needs a build system. Choose p5.js version deliberately: stable 1.x for broad compatibility; 2.x only when required by newer APIs or libraries.

Production pattern:

```text
CONCEPT → DESIGN → CODE → PREVIEW → EXPORT → VERIFY
```

Separate configuration, palette, mutable state, helpers, entity classes, and event handlers. Use seeded randomness for reproducibility. Disable the Friendly Error System and set pixel density intentionally for production. Build layered composition with offscreen graphics buffers; raw single-pass sketches usually look flat.

Performance rules:

- avoid DOM work and logging in `draw()`;
- batch points or use pixel buffers for large particle counts;
- keep transforms inside balanced `push()`/`pop()` scopes;
- use deterministic `noLoop()`/`redraw()` control for headless frame capture;
- verify sustained frame rate at target resolution.

Exports may be PNG, GIF, frame sequence, MP4 via ffmpeg, or SVG when the renderer supports it. Interactive deliverables need discoverable controls and graceful resize behavior.

## 5. Pretext Kinetic Typography

Use `@chenglou/pretext` when line breaks and grapheme positions must be known before rendering, especially for text flowing around animated geometry, word-based games, shatter effects, editorial layouts, or shrink-wrapped multiline UI.

Two core modes:

1. measure with `prepare()` + `layout()` and let CSS render;
2. measure segments and draw them yourself with `prepareWithSegments()`, `layoutWithLines()`, or streaming `layoutNextLineRange()`.

For variable-width flow, calculate the available corridor per row, ask Pretext for the next line range, materialize it, and advance the shared cursor. Cache prepared text+font handles; only layout should run per frame. Keep canvas and CSS font declarations exactly synchronized, use `Intl.Segmenter` for graphemes, and skip impossibly narrow rows instead of forcing one-character lines.

Use real, meaningful prose rather than lorem ipsum. Pin the CDN package version, serve locally for verification, inspect the browser console, and confirm both first-paint quality and 60fps behavior.

## Cross-Medium Export and QA

For every deliverable:

1. Render representative stills or open the live browser artifact.
2. Inspect visually at the intended resolution.
3. Check logs or browser console for silent failures.
4. Confirm exact dimensions, duration, frame rate, file format, and audio presence where applicable.
5. Exercise interactions and resize paths for browser artifacts.
6. Deliver the actual file path or media attachment, not just source code.

## Archived Source Packages

This umbrella absorbed and archived the complete original packages for `ascii-art`, `ascii-video`, `manim-video`, `p5js`, and `pretext`. Their original references, scripts, and templates remain intact and recoverable in the curator archive.