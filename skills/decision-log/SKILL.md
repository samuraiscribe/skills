---
name: decision-log
description: Adds the decisions made in a meeting to a running decision log, each with its date, context and the meeting it came from. Use it so you can always answer "when did we decide that, and why?".
metadata:
  suggested_trigger: "after_meeting"
  category: "Follow-up"
  tested_with: "local"
  version: "1.0"
  spec: "1"
---
Add this meeting's decisions to the decision log.

1. Get the meeting's title and day with get_meeting, and read its Summary with read_document.
2. Find the decisions: what the meeting clearly decided. If the Summary has a Decisions section, start from it, but keep only real decisions: a task someone will do ("Omar will fix the crash") is an action item, not a decision — leave it out. If there are none, say so in one line and stop: do not touch the log.
3. Write one entry per decision:

```
- **<day>** — <the decision, stated plainly>. *Why:* <the reason given, if one was>. (<meeting title>)
```

4. Look for the log with search_notes (query: `Decision log`).
   - If a note named `Decision log` exists, read it with read_note, then add the entries right under its first heading with edit_note: `old_text` is that first heading line, `new_text` is the heading line, a blank line, then the entries.
   - If not, create it with create_note at `Decision log.md`: a heading `# Decision log`, a blank line, then the entries.
5. Reply in one line with how many decisions you added.

Rules:
- A decision needs someone clearly deciding. A suggestion, a wish or a joke is not one, and neither is a task someone will do by a date.
- Never invent a reason: leave out *Why:* when none was said.
- Newest entries at the top.
- Write in the same language as the meeting.
