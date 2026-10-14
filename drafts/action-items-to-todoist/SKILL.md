---
name: action-items-to-todoist
description: Adds a meeting's action items to Todoist — one task each, with the due date that was said and a line saying which meeting it came from. Use it after a meeting whose tasks you keep in Todoist.
metadata:
  accepts: "meeting"
  requires: "todoist"
  tools: "todoist__find-projects, todoist__add-tasks"
  suggested_trigger: "after_meeting"
  category: "Follow-up"
  version: "0.1"
  spec: "1"
---
Add this meeting's action items to Todoist.

1. Get the meeting with get_meeting: note its title and date.
2. Read its Summary with read_document. Find the Action Items section.
   - If there is no Action Items section, or it lists nothing, reply "No action items to add." and stop. Do not call any Todoist tool.
3. Pick where they go: call todoist__find-projects with `searchText` set to the meeting's title. If one project's name matches the meeting well, use its id. Otherwise use "inbox".
4. Call todoist__add-tasks once, with `tasks` holding one entry per action item:
   - content: the task itself, short, starting with a verb, without the owner's name
   - description: `From the meeting "<meeting title>" on <date>. Owner as said in the meeting: <name>.` Where the owner is "Mic Speaker", write "you" instead: that is the user.
   - dueString: only when a day was said ("Friday", "next week", "June 3"), in the words that were said; leave it out otherwise
   - projectId: the id from step 3, or "inbox"
   Pass only these four. Never set a priority, a label or a person: nobody said one.
5. Reply with one line per task added. If Todoist refused one, say which and why.

Rules:
- Add only the items in the Summary's Action Items. Never invent a task, an owner or a date.
- One task per item, each added once.
- Write in the same language as the meeting.
