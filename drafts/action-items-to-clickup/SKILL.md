---
name: action-items-to-clickup
description: Turns a meeting's action items into ClickUp tasks — one task each, with a line saying who took it on and which meeting it came from. Use it after a meeting whose work your team tracks in ClickUp.
metadata:
  accepts: "meeting"
  requires: "clickup"
  tools: "clickup__clickup_get_workspace_hierarchy, clickup__clickup_create_task"
  suggested_trigger: "after_meeting"
  category: "Follow-up"
  version: "0.1"
  spec: "1"
---
Add this meeting's action items to ClickUp, one task each.

1. Get the meeting with get_meeting: note its title and date.
2. Read its Summary with read_document. Find the Action Items section.
   - If there is no Action Items section, or it lists nothing, reply "No action items to add." and stop. Do not call any ClickUp tool.
3. Call clickup__clickup_get_workspace_hierarchy. Pick the list whose name best matches the meeting's title; if none does, the first list. Note its id.
4. For each action item, call clickup__clickup_create_task once, with:
   - list: the list's id
   - name: the task itself, short, starting with a verb, without the owner's name
   - description: `From the meeting "<meeting title>" on <date>. Owner as said in the meeting: <name>.` — and the due date in words if one was said. Where the owner is "Mic Speaker", write "you" instead: that is the user.
   Never set an assignee, a priority or a status: nobody said one, and a name said in a meeting may not be the person's ClickUp account.
5. Reply with one line per task added, and the list they went to. If ClickUp refused one, say which and why.

Rules:
- Add only the items in the Summary's Action Items. Never invent a task, an owner or a date.
- One task per item, each added once.
- Write in the same language as the meeting.
