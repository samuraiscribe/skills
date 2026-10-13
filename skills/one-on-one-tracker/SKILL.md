---
name: one-on-one-tracker
description: After a one-on-one, adds what was discussed — topics, feedback, commitments, what to follow up next time — to a running note for that person. Use it for recurring 1:1s with your team or your manager.
metadata:
  suggested_trigger: "after_meeting"
  category: "Management"
  tested_with: "local"
  version: "1.0"
  spec: "1"
---
Add this one-on-one to the running note for the person it was with.

1. Read the meeting with get_meeting and its Summary with read_document. If it has no Summary, read it with read_transcript.
2. Work out who the other person is: a name in the title ("1:1 with Dana", "Dana / Karl"), else the other speaker's name. If you cannot tell, use "this person" and say so in your reply.
3. Write today's entry:

```
## <meeting day> — <meeting title>
**Topics:** one line per topic.
**Feedback:** given or received, if any.
**Commitments:** `- [ ] **Owner** — task` for each.
**Next time:** what to follow up on.
```

Topics: every subject they talked about, one line each. Commitments: only what someone agreed to do, with who and when as said. Leave out any other line with nothing in it.

4. Look for the running note with search_notes (query: `1-on-1 <person>`).
   - If a note named `1-on-1 — <person>` exists, read it with read_note, then add today's entry right under its first heading with edit_note: `old_text` is that first heading line, `new_text` is the heading line, a blank line, then the entry.
   - If not, create it with create_note at `1-on-1 — <person>.md`: a heading `# 1-on-1 — <person>`, a blank line, then the entry.
5. Reply in one line saying what you added and where.

Rules:
- Use only what was said. Never invent feedback, commitments or dates.
- Newest entry at the top.
- A note's name never contains `/` or `:`.
- Write in the same language as the meeting.
