---
name: follow-up-email
description: Drafts a follow-up email after a meeting — thanks, what was decided, who does what by when, and next steps. Use it after a call with a client, a candidate or a partner.
metadata:
  accepts: "meeting"
  suggested_trigger: "after_meeting"
  document: "Follow-up email"
  category: "Follow-up"
  version: "1.1"
  spec: "1"
---
Draft a follow-up email for this meeting.

1. Get the meeting with get_meeting: note its title, who spoke, and its `folder` line.
2. Read its Summary with read_document. If it has none, read the meeting with read_transcript.
3. Write the email in plain text, as it would be sent — no Markdown, no `**`:

A subject: short, naming the meeting's topic.

Then the body:
- One line thanking them for the time, naming the topic.
- `What we agreed:` then each decision that was clearly made, one `- ` line each. A task someone will do is not a decision: it goes under Next steps. If nothing was decided, leave this heading out entirely.
- `Next steps:` then each action item as `- Name — task`, with a date only if one was said. Where the name would be "Mic Speaker", write `I` instead — that is the user. If nobody took on anything, leave this heading out entirely.
- One closing line about the next step or the next meeting, if one was mentioned.

4. Before saving, check the email: no "Mic Speaker", and no heading followed by "no decisions" or "no action items".
5. Hand it over:
   - If you have the write_document tool, reply with the email itself and nothing else — `Subject: …` on the first line, then the body: it is saved for you.
   - Otherwise call draft_email once with `subject` and `body`. Leave `to` out: a name said in a meeting is not an email address. Then reply in one line saying the draft is ready to open. Do not put the email in your reply.

Rules:
- Use only what was said in the meeting. Never invent a decision, a task, a date, a price or a name. A section with nothing in it is left out.
- The email is from the user. Lines labelled "Mic Speaker" are theirs: write their own tasks as `I — task`, never "Mic Speaker".
- A section with nothing in it is left out, heading and all: never write "no decisions" or "no action items".
- Keep it short: an email someone would actually send. No more than about 150 words in the body.
- Write in the same language as the meeting. Use a friendly, professional tone.
- Do not sign it with a name; the user adds their own.
