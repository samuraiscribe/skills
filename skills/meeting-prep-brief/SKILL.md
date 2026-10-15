---
name: meeting-prep-brief
description: Before a meeting, writes a one-page brief from the last time you met the same people — who is coming, what happened last time, open action items, open questions. Use it to get ready for a follow-up meeting.
metadata:
  accepts: "calendar_event, meeting"
  suggested_trigger: "before_meeting 15"
  category: "Preparation"
  tested_with: "local"
  version: "1.3"
  spec: "1"
---
Write a short brief to prepare for a meeting.

1. Find "last time" — one meeting, read once:
   - **You were given a meeting:** that meeting *is* last time. Read its Summary with read_document, then go straight to step 2. Do not call search or list_meetings at all.
   - **No meeting was given, and a calendar meeting is described above:** its description ends by saying which earlier meetings were with the same people. Read the Summary of the first one it lists with read_document. If it says there is no earlier meeting with them, the brief is just `## Who's coming` and, under it, `First time meeting — nothing earlier in your notes.` — no other sections. Do not call search or list_meetings.
   - **The calendar meeting names no other attendees:** make one search call with the main words of its title. Take the most recent meeting it finds that is really about the same thing and read its Summary with read_document. If it finds none, say so in one line and stop.
2. Save the brief with create_note at `Prep — <meeting title>.md` (leave any `/` or `:` out of the name), with these sections, only the ones you have something for:

## Who's coming
Only when a calendar meeting is described above: one line naming its attendees other than the user, with their role or company if the earlier meeting said it. Otherwise leave this heading out.

## Last time
Two or three sentences on what was discussed and how it ended.

## Open action items
`- [ ] **Owner** — task`, for each task someone took on that has not come up as done since.

## Open questions
Questions someone asked that were not answered or settled.

## Worth raising
One or two points to bring up, based only on what was said before.

3. Only after create_note has answered, reply in one line saying the brief is ready to review. Do not put the brief in your reply, and never say it is saved before create_note has answered.

Rules:
- One meeting is enough. At most one search call, and only when the calendar meeting names no other attendees.
- Leave out a section with nothing in it, heading and all. Never write "None", "N/A", "To be added" or the like.
- Write the user's own tasks as **You**, never "Mic Speaker". Never list a transcript label such as "Speaker 2" as a person.
- Use only what is in the meeting you read. Never invent facts, dates or names.
- Keep the brief under about 250 words.
- Write in the same language as the meetings.
