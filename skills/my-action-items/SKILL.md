---
name: my-action-items
description: Collects everything you committed to in the past two weeks of meetings into one list, with the meeting each came from. Use it to see what you still owe people.
metadata:
  accepts: "none"
  suggested_trigger: "schedule weekdays 08:30"
  category: "Review"
  tested_with: "local"
  version: "1.1"
  spec: "1"
---
List what the user committed to in their recent meetings.

1. Find out who the user is: read_memory may give their name. In meetings recorded with two tracks, the user's own lines are labelled "Mic Speaker".
2. List the meetings from the past fourteen days with list_meetings (`from` = fourteen days ago, `to` = today, dates as YYYY-MM-DD). If there are none, say so in one line and stop.
3. For each meeting, read its Summary with read_document and take the action items owned by the user: their name, "Mic Speaker", or "I" said by them.
4. If you found none, say so in one line and stop.
5. Otherwise save the list with create_note at `My action items — <today>.md`:

```
## Open
- [ ] task (meeting title, day)
```

Newest meetings first. Put a due date at the start of a line only when one was said.

6. Reply with the number of items and the list itself.

Rules:
- Only items the user clearly took on. Not other people's tasks, not suggestions, not wishes.
- Never invent a task, a person or a date.
- Write in the same language as the meetings.
