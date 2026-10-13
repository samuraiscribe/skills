---
name: weekly-review
description: Reviews the past seven days of meetings in one note — what each was about, the decisions made, open action items and loose ends. Use it on Monday mornings, or whenever you want to catch up on a week.
metadata:
  suggested_trigger: "schedule monday 09:00"
  category: "Review"
  tested_with: "local"
  version: "1.0"
  spec: "1"
---
Write a review of the past seven days of meetings.

1. List the meetings from the past seven days with list_meetings (`from` = seven days ago, `to` = today, dates as YYYY-MM-DD).
2. If there are none, say so in one line and stop.
3. For each meeting, read its Summary with read_document, using the meeting's id. A meeting with no Summary is listed by title only.
4. Save the review with create_note at `Weekly review — <first day> to <last day>.md`, days as YYYY-MM-DD, with these sections, only the ones you have something for:

## Meetings
One line per meeting: `**Title** (day) — what it was about, in one sentence.`

## Decisions
Every decision clearly made, with the meeting it came from in brackets.

## Open action items
`- [ ] **Owner** — task (meeting)`, for every action item.

## Loose ends
Questions left open, and topics that came up in more than one meeting without being settled.

5. Only then reply, in one line, saying the review is ready, with how many meetings it covers. Do not put the review in your reply: it is done only once saved with create_note.

Rules:
- Use only what the Summaries say. Never invent decisions, tasks or names.
- Never write "None" under a heading: leave the section out.
- Write in the same language as the meetings.
