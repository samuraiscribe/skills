---
name: book-a-follow-up
description: Drafts a follow-up email with a Calendly link for booking the next meeting — what was agreed, the next steps, and a one-time scheduling link. Use it after a call that should lead to another one.
metadata:
  accepts: "meeting"
  requires: "calendly"
  tools: "calendly__users-get_current_user, calendly__event_types-list_event_types, calendly__scheduling_links-create_single_use_scheduling_link"
  category: "Follow-up"
  version: "0.1"
  spec: "1"
---
Draft a follow-up email for this meeting, with a link to book the next one.

1. Get the meeting with get_meeting: note its title and who spoke.
2. Read its Summary with read_document. If it has none, read the meeting with read_transcript.
3. Call calendly__users-get_current_user, then calendly__event_types-list_event_types for that user. Pick the active event type whose name best fits a follow-up (a "follow-up", "call" or "meeting" of 30 minutes or so); else the first active one.
   - If there is none, write the email without a link and say so in your reply.
4. Call calendly__scheduling_links-create_single_use_scheduling_link for that event type, for one booking. Note the link it gives.
5. Write the email in plain text, as it would be sent — no Markdown:
   - One line thanking them for the time, naming the topic.
   - `Next steps:` then each action item as `- Name — task`. Where the name would be "Mic Speaker", write `I` — that is the user. Leave this out if nobody took anything on.
   - One line inviting them to pick a time for the next meeting, then the link on its own line.
6. Call draft_email once with `subject` and `body`. Leave `to` out. Then reply in one line saying the draft is ready to open.

Rules:
- Use only what was said in the meeting. Never invent a task, a date or a name.
- Keep it short: about 120 words in the body. Do not sign it; the user adds their own.
- Create one link, once. Write in the same language as the meeting.
