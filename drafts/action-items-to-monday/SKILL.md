---
name: action-items-to-monday
description: Adds a meeting's action items to a monday.com board — one item each, with a note of who took it on and which meeting it came from. Use it after a meeting whose work your team tracks on monday.com.
metadata:
  accepts: "meeting"
  requires: "monday"
  tools: "monday__search, monday__get_board_schema, monday__create_item"
  suggested_trigger: "after_meeting"
  category: "Follow-up"
  version: "0.1"
  spec: "1"
---
Add this meeting's action items to a monday.com board, one item each.

1. Get the meeting with get_meeting: note its title and date.
2. Read its Summary with read_document. Find the Action Items section.
   - If there is no Action Items section, or it lists nothing, reply "No action items to add." and stop. Do not call any monday.com tool.
3. Find the board: call monday__search with `searchType` "BOARD" and `searchTerm` set to the meeting's title. If nothing comes back, search again with one key word from the title. If there is still no board, reply "I could not find a monday.com board for this meeting — tell me which one to use." and stop.
4. Call monday__get_board_schema with that board's id. Use the board's first group.
5. For each action item, call monday__create_item once, with:
   - boardId: the board's id
   - groupId: the first group's id
   - name: the task itself, short, starting with a verb, without the owner's name
   - columnValues: "{}"
   Never set a person, a status or a date column: a name said in a meeting may not be the person's monday.com account.
6. Reply with one line per item added, then one line: `Owners as said in the meeting:` and each `task — name`. Where the owner is "Mic Speaker", write "you": that is the user. If monday.com refused one, say which and why.

Rules:
- Add only the items in the Summary's Action Items. Never invent a task, an owner or a date.
- One item per action item, each added once.
- Write in the same language as the meeting.
