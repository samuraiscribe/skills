---
name: call-notes-to-attio
description: Logs a call in Attio — a note on the company or person it was with, holding the summary, and a task for each follow-up you took on. Use it after a sales or customer call.
metadata:
  accepts: "meeting"
  requires: "attio"
  tools: "attio__search-records, attio__create-note, attio__create-task"
  suggested_trigger: "after_meeting"
  category: "Sales"
  version: "0.1"
  spec: "1"
---
Log this call in Attio.

1. Get the meeting with get_meeting: note its title, date and who spoke.
2. Read its Summary with read_document.
   - If it has no Summary, reply "This meeting has no summary yet — process it first." and stop. Do not call any Attio tool.
3. Find who the call was with: the company named in the meeting's title, else the one the Summary names most. Call attio__search-records for it among companies.
   - If no company is found, try the person's name among people.
   - If nothing is found, reply "I could not find who this call was with in Attio — tell me the company." and stop. Never create a record.
4. Call attio__create-note once on that record:
   - title: `<meeting title> — <date>`
   - content: the Summary, as Markdown, exactly as it is
5. For each action item in the Summary whose owner is "Mic Speaker" (that is the user), call attio__create-task once:
   - content: the task, short, starting with a verb
   - linked to the same record
   - a deadline only when a calendar date was said
   Items owned by someone else are in the note already; make no task for them.
6. Reply with one line naming the record the note went on, then one line per task.

Rules:
- Never invent a company, a person, a task or a date. Never create or change a company or person record.
- One note, and one task per item, each created once.
- Write in the same language as the meeting.
