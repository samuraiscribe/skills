---
name: lecture-study-guide
description: Turns a recorded lecture or talk into a study guide — key concepts, definitions, examples, and practice questions with answers. Use it after a class, a course video or a talk you want to learn from.
metadata:
  document: "Study guide"
  category: "Learning"
  tested_with: "local"
  version: "1.0"
  spec: "1"
---
Write a study guide for this lecture.

1. Read the lecture with read_transcript, from the start to the end. For a long lecture, use digest_transcript if you have it, asking for the concepts, definitions and examples.
2. Write the guide, in Markdown:

## Overview
Two or three sentences: what the lecture is about and its main point.

## Key concepts
One bullet per concept, explained in one or two plain sentences.

## Definitions
`**Term** — definition`, for each term the lecturer defined.

## Examples
The examples the lecturer used, each with the concept it illustrates.

## Practice questions
Five to eight questions that test understanding, not memory, each followed by its answer:

```
1. Question?
   **Answer:** the answer, in one or two sentences.
```

3. Save it:
   - If you have the write_document tool, reply with the guide itself and nothing else: it is saved for you.
   - Otherwise, save the guide with create_note at `<folder>/Study guide.md`, where `<folder>` is exactly the path on get_meeting's `folder` line. Then reply in one line saying it is ready.

Rules:
- Use only what the lecture said. Answers must come from the lecture, not general knowledge.
- The transcript is machine-made and may mishear terms: where the intended word is obvious, spell it right.
- Leave out a section with nothing in it.
- Write in the same language as the lecture.
