---
name: media-content-workflows
description: "Find, extract, transform, and package online media content: Tenor GIF search/download and YouTube transcript summaries, chapters, quotes, threads, and articles."
version: 1.0.0
author: Hermes Agent
license: MIT
platforms: [linux, macos, windows]
metadata:
  hermes:
    tags: [media, gif, tenor, youtube, transcript, summary, chapters, quotes, thread, blog]
---

# Media Content Workflows

Use this umbrella when the task is to retrieve online media or transform media-derived text into a reusable deliverable. Route by source and desired output.

## Routing

- Reaction or topical GIF discovery/download → Tenor GIF workflow.
- YouTube transcript extraction, summarization, chapters, quotations, X thread, or blog article → YouTube content workflow.
- If the task instead creates original animation or generative art, use `creative-production-workflows`.

## 1. Tenor GIF Search and Download

Prerequisites are `curl`, JSON parsing support such as `jq`, and `TENOR_API_KEY` configured outside chat. Never expose the key in output.

Workflow:

1. Convert the user’s intent into a concise search phrase.
2. Query Tenor v2 search with a conservative result limit and appropriate content filter.
3. Compare titles, dimensions, and available media formats.
4. Prefer `tinygif`/`tinymp4` for lightweight chat previews and full `gif` or `mp4` for downloads.
5. Download with redirect following and verify the file exists and has a plausible media type before sending.

Relevant API fields live under each result’s `media_formats`, including `gif`, `tinygif`, `mp4`, `tinymp4`, `webm`, and `nanogif`. URL-encode queries rather than interpolating unsafe raw text. Present a small set of options when tone is subjective; do not assume the first result is best.

## 2. YouTube Transcript Extraction

Accept standard watch URLs, short URLs, Shorts, embeds, live URLs, or raw video IDs. Use a transcript-fetch helper or `youtube-transcript-api`, then validate that text is non-empty and in the expected language.

Retry order:

1. requested language chain;
2. any available transcript;
3. report that captions are disabled, private, or unavailable if extraction still fails.

For long transcripts, split into overlapping semantic chunks, summarize each, then synthesize. Preserve timestamps through the pipeline when the output needs chapters or quotes.

## 3. Transformation Formats

### Summary

Provide the thesis, major arguments, evidence, and practical takeaways. Separate what the speaker claimed from your own synthesis.

### Timestamped chapters

Group around real topic shifts, not arbitrary intervals. Use a concise title and one-line description per chapter.

### Quotations

Use exact transcript text where available, include timestamps, and avoid polishing a paraphrase into quotation marks.

### X thread

Build a coherent numbered progression with one idea per post and platform-appropriate length. Preserve nuance rather than flattening the entire video into slogans.

### Blog article

Create a standalone title, introduction, section hierarchy, examples, and takeaways. Attribute the source and distinguish direct quotes from paraphrase.

## Verification

Before delivery:

- confirm source URL or media identity;
- verify transcript language and non-empty content;
- check timestamps against extracted segments;
- remove duplicated overlap from chunk synthesis;
- verify GIF/video download path, format, and size;
- match the requested output format exactly;
- attach or link the actual artifact when the user requested a file.

## Archived Source Packages

This umbrella absorbed and archived the complete original packages for `gif-search` and `youtube-content`, preserving the transcript helper script and output-format reference in the curator archive.