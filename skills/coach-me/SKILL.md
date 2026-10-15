---
name: coach-me
description: Gives you honest, specific feedback on how you came across in a meeting — how much you talked, how you listened and asked questions, how clearly you explained — with real moments from the conversation and two or three things to try next time. Use it after a sales call, an interview you ran, a 1:1 or a presentation you want to get better at.
metadata:
  accepts: "meeting"
  category: "Coaching"
  tested_with: "local"
  version: "1.1"
  spec: "1"
---
Give the user feedback on how they did in this meeting.

1. Call speaker_stats for this meeting. Its line "the user is:" says which speaker is the user.
   - If the meeting has no transcript, say so in one line and stop.
   - If it says the user is NOT KNOWN: do not guess. Unless the user has told you their name and it is one of the speakers, reply with one line asking which speaker they were, naming the speakers, and stop.
2. speaker_stats ends with what the user said: their questions and how their longest stretches began, each with its time. **Only those lines are the user's.** Everything else in the meeting was said by other people — never credit the user with it.
3. Read the conversation with read_transcript, so you know what each of the user's lines answered and what came after it. For a long meeting, read just before and after each of the user's lines (from_seconds and to_seconds), not the whole meeting.
4. Pick the moments that matter: 2 or 3 of the user's lines that went well, and 2 or 3 that could have gone better. Each must be one of the user's lines from step 2, with its time.
5. Write the feedback in Markdown:

## How the talking was shared
Two sentences from speaker_stats: the user's share of the talking against the others', their longest stretch without a break and when it was, and how many questions they asked. Say whether that suited this kind of meeting: in a sales call, a discovery call or an interview the user ran, the other side should do most of the talking; in a presentation or a training, the user should.

## What went well
2–3 bullets. Each: the user's line and its time, and why it worked.

## What to try next time
2–3 bullets. Each: the moment, with its time; what happened; and one concrete thing to do instead — a sentence the user could actually say.

Rules:
- Speak to the user as "you". Give feedback on the user only, never on the others.
- Every point is one of the user's own lines, with its time. Never invent a quote, a time or a number, and never use another speaker's words as the user's. Quote a few words at most.
- If questions were "not measured", do not say how many the user asked.
- Be direct and kind, like a good coach. No general advice ("communicate clearly") without a moment behind it.
- If the user said less than a minute in total, say there is too little to judge and give only the talk-time numbers.
- Keep it under 250 words. Write in the same language as the meeting.
