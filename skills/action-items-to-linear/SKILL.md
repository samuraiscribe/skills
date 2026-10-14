---
name: action-items-to-linear
description: Files a meeting's action items in Linear — one issue per task, with the owner and due date that were said and a line saying which meeting it came from. Use it after a meeting whose tasks your team tracks in Linear.
metadata:
  accepts: "meeting"
  requires: "linear"
  tools: "linear__list_teams, linear__save_issue"
  suggested_trigger: "after_meeting"
  category: "Follow-up"
  version: "1.0"
  spec: "1"
---
File this meeting's action items in Linear, one issue each.

1. Get the meeting with get_meeting: note its title and date.
2. Read its Summary with read_document. Find the Action Items section.
   - If there is no Action Items section, or it lists nothing, reply "No action items to file." and stop. Do not call any Linear tool.
3. Find the team with linear__list_teams. If there is one team, use it. If there are several, use the one whose name best matches the meeting's title, else the first.
4. For each action item, call linear__save_issue once, with:
   - team: the team's id
   - title: the task itself, short, starting with a verb, without the owner's name
   - description: `From the meeting "<meeting title>" on <date>. Owner as said in the meeting: <name>.` — and the due date in words if one was said. Where the owner is "Mic Speaker", write "you" instead: that is the user.
   - dueDate: only when the item gives a calendar date, as YYYY-MM-DD; leave it out for "Friday" or "next week"
   Pass only these four. Never pass an id (that would change an existing issue), never set an assignee (a name said in a meeting may not be the person's Linear account), and never set a priority (nobody said one).
5. Reply with one line per issue: its title and the identifier Linear gave it (like ENG-123). If Linear refused one, say which and why.

Rules:
- File only the items in the Summary's Action Items. Never invent a task, an owner or a date.
- One issue per item, each filed once.
- Write in the same language as the meeting.
