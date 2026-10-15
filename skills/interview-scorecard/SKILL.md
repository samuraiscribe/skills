---
name: interview-scorecard
description: Turns a job interview you ran into a scorecard — a rating for each area with evidence and times from the conversation, strengths, concerns, what the candidate asked, notice period and salary if they came up, and a suggested recommendation for you to confirm. Use it after an interview, before you fill in your hiring system.
metadata:
  accepts: "meeting"
  suggested_trigger: "after_meeting"
  document: "Interview scorecard"
  category: "Recruiting"
  tested_with: "local"
  version: "1.4"
  spec: "1"
---
Write an interview scorecard for this meeting.

1. Get the meeting with get_meeting: note its `folder` line and who spoke. The candidate is the person being asked about their experience; the user ("Mic Speaker") is the interviewer.
2. If it was not a job interview — nobody is being assessed for a role — say so in one line and stop. Do not create, change or delete anything.
3. If the meeting has a Notes document, read it with read_document. If it lists what to assess (skills, competencies, a rubric), those are the areas. Otherwise the areas are: Role skills, Problem solving, Communication, Ownership, Motivation.
4. Read the interview with read_transcript, from the start to the end. For a long meeting, use digest_transcript if you have it, asking for evidence for each area, the candidate's questions, and any notice period, start date or salary.
5. Write the scorecard in Markdown, with these sections — leave out any with nothing in it:

# Interview scorecard — <candidate's name>, <role>

## Summary
Two sentences: who the candidate is and the overall picture. Refer to the candidate by name or as "they".

## Ratings
One line per area: the rating, then in a few words what the candidate said or did that shows it, then the time — for example `- **Problem solving** — Strong: designed a per-customer rate limiter that fails open if Redis is down (2:14)`. Ratings are Strong, Good, Mixed, Weak or Not covered; an area that never came up is "Not covered", with no evidence.

## Strengths
Bullets, each with what the candidate said or did and its time.

## Concerns
Bullets, each with evidence and its time. Gaps the candidate admitted count.

## Their questions
What the candidate asked.

## Logistics
Notice period or start date, salary, location — only what was said, numbers exactly as said.

## Next steps
Only what was agreed.

## Suggested recommendation
Follow from the ratings: **Strong yes** if every area is Strong or Good and no concern is serious; **Yes** if most are Strong or Good; **Lean no** if one area is Weak or one concern is serious for this role; **No** if several are. Then one sentence saying why. Then on its own line: `This is a suggestion from the conversation alone; the decision is yours.`

6. Save it:
   - If you have the write_document tool, reply with the scorecard itself and nothing else: it is saved for you.
   - Otherwise save it with create_note. The path is the value of get_meeting's `folder` line, exactly as written, then `/Interview scorecard.md` — for example `Meetings/2026-10-15 Interview — Jordan Patel/Interview scorecard.md`. Not Notebooks, not Unfiled, and no other name: the scorecard belongs with the interview. Then reply in one line saying it is ready to review.

Rules:
- Use only what was said. Never invent experience, a number, a salary or a date.
- Write every time as plain text in round brackets, as `(1:06)` — never as a link, `[[1:06]]` or `[1:06]`.
- Judge only what bears on the job. Leave out age, family, health, religion, nationality, accent and appearance, even if they came up.
- Do not say a decision was made unless the interviewer said so.
- The role is as the meeting's title or the interviewer names it; leave it out if neither does. Never add to it.
- Call the candidate by their name or "they" throughout.
- Logistics only as said: leave out anything not mentioned rather than writing "not specified".
- Under 400 words. Write in the same language as the interview.
