---
name: web-design-prototyping
description: "Use when creating visual web artifacts: one-off HTML mockups, design variants, DESIGN.md token specs, and borrowing real product design-system references."
version: 1.0.0
author: Hermes Agent
license: MIT
platforms: [linux, macos, windows]
metadata:
  hermes:
    tags: [design, html, prototype, mockup, design-systems, tokens]
    related_skills: [p5js, pretext, architecture-diagram]
---

# Web Design & Prototyping

## Overview

Umbrella for browser-viewable design artifacts: quick HTML mockups, polished one-off pages/decks/prototypes, design-token specs, and real-world design-system references.

## When to Use

- User asks for a landing page, product mockup, deck-like HTML artifact, or interactive prototype.
- User wants multiple design directions to compare.
- User asks to author/validate/export a `DESIGN.md` token spec.
- User wants to imitate or learn from a recognizable product design system.

## Modes

### Quick Sketches

Use for throwaway mockups or 2-3 variants. Optimize for speed and visual contrast between options.

### Polished HTML Artifact

Use when the output should be presentation-ready. Include typography, spacing, responsive behavior, and real content hierarchy; avoid generic AI gradients unless requested.

### Design-System Reference

Use real product references (e.g. Stripe, Linear, Vercel, Apple, Notion) as style constraints, not copied content. State which tokens/patterns are borrowed.

### DESIGN.md Token Specs

Use when the deliverable is a portable design spec rather than a page. Include color, type, spacing, radius, shadow, motion, and component rules.

## Workflow

1. Clarify artifact purpose only if missing; otherwise choose a sensible default.
2. Create a self-contained HTML/CSS/JS file or DESIGN.md.
3. Use real content structure; avoid lorem ipsum unless user requests placeholder content.
4. Open/render or validate when possible.
5. Iterate based on screenshots or user feedback.

## Verification Checklist

- [ ] Artifact exists at a concrete path or URL.
- [ ] It renders without console errors when browser-tested.
- [ ] Visual hierarchy, spacing, and responsive behavior are checked.
- [ ] Design references are named and used as constraints, not plagiarism.

## Consolidated Legacy Skills

Absorbed `claude-design`, `sketch`, `popular-web-designs`, and `design-md`. Preserve highly reusable templates as files under this umbrella rather than standalone skills.
