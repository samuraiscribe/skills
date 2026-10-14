---
name: sales-call-notes
description: Turns a sales or discovery call into structured notes — the customer's pain, who decides, budget, timeline, objections and the agreed next step. Use it after a call with a prospect or customer.
metadata:
  accepts: "meeting"
  suggested_trigger: "after_meeting"
  document: "Sales call notes"
  category: "Sales"
  tested_with: "local"
  version: "1.1"
  spec: "1"
---
Write sales call notes for this meeting.

1. Get the meeting with get_meeting: note its `folder` line. Then read it with read_transcript, from the start to the end. For a long meeting, use digest_transcript if you have it, asking for the sections below.
2. If it was not a sales or customer call — nobody is buying or being sold to — say so in one line and stop.
3. Write the notes, in Markdown, with these sections — only the ones the call actually covered:

## Company and people
Who was on the call from their side, with their role if said.

## Pain
The problems they want solved, in their words where possible.

## Current situation
What they use or do today.

## Decision
Who decides, how they decide, and anyone else who must agree.

## Budget
Any amount, range or constraint that was said.

## Timeline
When they want to decide or start, and why.

## Objections and risks
Concerns they raised, and how they were answered.

## Next step
What was agreed to happen next, by whom, and when — times exactly as said.

4. Save it:
   - If you have the write_document tool, reply with the notes themselves and nothing else: they are saved for you.
   - Otherwise save them with create_note at `<folder>/Sales call notes.md`, where `<folder>` is exactly the path on get_meeting's `folder` line. Then reply in one line saying they are ready to review.

Rules:
- Use only what was said. Never guess a budget, a timeline or a decision maker.
- Leave out a section with nothing in it, heading included.
- Bullet points, short.
- Write in the same language as the meeting.
