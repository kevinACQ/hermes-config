---
name: ai-audio-music
description: "Use when creating, analyzing, or iterating on AI music/audio: lyrics and song prompts, Suno-like generation, AudioCraft/MusicGen, and spectrogram/audio-feature inspection."
version: 1.0.0
author: Hermes Agent
license: MIT
platforms: [linux, macos, windows]
metadata:
  hermes:
    tags: [audio, music, songwriting, suno, musicgen, spectrogram]
    related_skills: [youtube-content]
---

# AI Audio & Music

## Overview

Class-level umbrella for music/audio generation and analysis. It covers songwriting craft, Suno/HeartMuLa-style prompt packages, AudioCraft/MusicGen generation, and audio feature visualization with spectrogram/chroma/MFCC tools.

## When to Use

- User asks for lyrics, song structure, genre tags, or AI music prompts.
- User wants to generate music or sound from text.
- User wants to analyze an audio file's spectrogram, tempo, features, or structure.
- User wants to iterate from a generated clip into a better prompt.

## Modes

### Songwriting & Prompting

- Capture genre, mood, vocalist, era, instrumentation, tempo, and structure.
- Separate lyrics from style tags.
- Use section markers (`[Verse]`, `[Chorus]`, `[Bridge]`) when the target generator benefits from them.

### Suno-like Generation

- Produce a compact tag set plus lyrics/assets bundle.
- Keep prompt constraints concrete: instrumentation, production, vocal style, mix references.

### AudioCraft / MusicGen

- Use when local or Python-based generation is appropriate.
- Check model availability and hardware first; generation can be slow/heavy.
- Save outputs to concrete paths and report them as media artifacts.

### Audio Analysis

- Use spectrograms/features to diagnose arrangement, timing, noise, or similarity.
- Summarize what the visualization implies musically, not just the raw feature names.

## Verification Checklist

- [ ] Lyrics/tags are separated when needed.
- [ ] Generated media path/URL is real and deliverable.
- [ ] Analysis cites actual audio-tool output.
- [ ] Iteration notes explain what changed and why.

## Consolidated Legacy Skills

Absorbed `songwriting-and-ai-music`, `heartmula`, `audiocraft-audio-generation`, and `songsee`.
