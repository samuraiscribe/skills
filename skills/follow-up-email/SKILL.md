---
name: follow-up-email
description: Drafts a follow-up email after a meeting, addressed to the people who were invited — thanks, what was decided, who does what by when, and next steps. Use it after a call with a client, a candidate or a partner.
metadata:
  accepts: "meeting"
  suggested_trigger: "after_meeting"
  document: "Follow-up email"
  category: "Follow-up"
  tested_with: "local"
  version: "1.5"
  spec: "1"
---
Draft a follow-up email for this meeting.

1. Get the meeting with get_meeting. Note its id, its title, who spoke, and its `attendees` line if it has one. The attendee marked `(you)` is the user.
2. Read its Summary with read_document. Only if the meeting has no Summary, read it with read_transcript instead.
3. Work out what you have, before writing anything:
   - **Decisions**: only what the Summary lists under a decisions heading, or what the transcript clearly settles ("we'll ship on the 20th"). If the Summary has no decisions heading, there are **no decisions**. Something to consider, revisit or decide later is not a decision — leave it out. A task someone will do is not a decision either: it is a next step.
   - **Next steps**: only tasks someone said they would do. If the Summary has no action items heading, there are **no next steps**.
   - **Recipients**: every address on the `attendees` line except the one marked `(you)`. No `attendees` line means no recipients.
4. Write the email in plain text, as it would be sent — no Markdown, no `**`:

A subject: short, naming the meeting's topic.

Then the body:
- One line thanking them for the time, naming the topic.
- Only if there are decisions: `What we agreed:` then each one on a `- ` line.
- Only if there are next steps: `Next steps:` then each as `- Name — task`, with a date only if one was said. The user's own tasks — "Mic Speaker", or the attendee marked `(you)` — are written `I — task`.
- If there are neither, one or two lines on what was discussed instead.
- One closing line about the next step or the next meeting, if one was mentioned.

5. Check the email before handing it over. Remove anything that fails:
   - no "Mic Speaker";
   - no heading followed by "none", "no decisions" or "no action items";
   - no placeholder in brackets, such as `[date]` or `[Name]`;
   - no signature or name at the end.
6. Hand it over with draft_email: `meeting_id`, `subject`, `body`, and `to` set to the recipients, comma-separated — leave `to` out if there are none. draft_email is how the email reaches the user, with recipients or without. If it refuses the draft, fix what it names and call it again. Then reply in one line saying who the draft is for and that it is ready to open. Do not put the email in your reply.

   (Only in a meeting's processing, where there is a write_document tool and no draft_email: reply with the email itself and nothing else — `To: <recipients>` on the first line if there are any, then `Subject: …`, then the body. It is saved for you.)

Rules:
- Use only what was said in the meeting. Never invent a decision, a task, a date, a price or a name. A section with nothing in it is left out, heading and all.
- An address comes only from the `attendees` line. A name said in the meeting is not an address.
- Where a person's name is not known, leave the name out rather than writing a label such as "Speaker 2".
- The email is from the user, so it never goes to them: leave the `(you)` address out of `to`.
- Keep it short: an email someone would actually send. No more than about 150 words in the body.
- Write in the same language as the meeting. Use a friendly, professional tone.
